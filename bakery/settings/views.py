# -*- coding: utf-8 -*-
import datetime
try:
    import simplejson as json
except ImportError:
    import json
import logging
from flask.ext.babel import gettext as _

from flask import Blueprint, render_template, request, flash, g, redirect, url_for, session, Markup

from ..extensions import github, db
from ..decorators import login_required
from .models import ProjectCache
from ..project.models import Project
from ..tasks import git_clone, git_clean

settings = Blueprint('settings', __name__, url_prefix='/settings')

@login_required
@settings.route('/', methods=['GET'])
def repos():
    _repos = None
    cache = ProjectCache.query.filter_by(login=g.user.login).first()
    myprojects = Project.query.filter_by(login=g.user.login, is_github=True).all()
    mygit = Project.query.filter_by(login=g.user.login, is_github=False).all()

    p = {}
    if myprojects:
        for i in myprojects:
            p[i.full_name] = i
    #import ipdb; ipdb.set_trace()
    return render_template('settings/repos.html',
        cache = cache,
        projects = p,
        gitprojects = mygit
    )

@login_required
@settings.route('/update', methods=['POST'])
def update():
    auth = github.get_session(token = session['token'])
    if g.user is not None:
        resp = auth.get('/user/repos', data = {'type': 'public'})
        if resp.status_code == 200:
            _repos = resp.json()
            cache = ProjectCache.query.filter_by(login=g.user.login).first()
            if not cache:
                cache = ProjectCache()
                cache.login = g.user.login

            cache.data = _repos
            cache.updated = datetime.datetime.utcnow()

            db.session.add(cache)
            db.session.commit()
            flash(_('Repositories refreshed.'))
        else:
            flash(_('Unable to load repos list.'))
    return redirect(url_for('settings.repos')+"#tab_massgithub")

@login_required
@settings.route('/profile', methods=['GET', 'POST'])
def profile():
    auth = github.get_session(token = session['token'])
    _repos = None
    if g.user is not None:
        resp = auth.get('/user/repos', data = {'type': 'public'})
        if resp.status_code == 200:
            _repos = resp.json()
        else:
            flash(_('Unable to load repos list.'))
    return render_template('settings/repos.html', repos=_repos)

HOOK_URL = 'http://requestb.in/nrgo4inr'

@login_required
@settings.route('/addhook/<path:full_name>') #, methods=['GET'])
def addhook(full_name):
    auth = github.get_session(token = session['token'])
    old_hooks = auth.get('/repos/%s/hooks' % full_name)
    if old_hooks.status_code != 200:
        logging.error('Repos API reading error for user %s' % g.user.login)
        flash(_('GitHub API access error, please try again later'))
        return redirect(url_for('settings.repos'))

    exist_id = False
    if old_hooks.json():
        for i in old_hooks.json():
            if i.has_key('name') and i['name'] == 'web':
                if i.has_key('config') and i['config'].has_key('url') \
                    and i['config']['url'] == HOOK_URL:
                    exist_id = i['id']

    if exist_id:
        logging.warn('Delete old webhook for user %s, repo %s and id %s' % (g.user.login, full_name, exist_id))
        resp = auth.delete('/repos/%(full_name)s/hooks/%(id)s' % {'full_name': full_name, 'id': exist_id})
        if resp.status_code != 204:
            flash(_('Error deleting old webhook, delete if manually or retry'))
            return redirect(url_for('settings.repos'))

    resp = auth.post('/repos/%(full_name)s/hooks' % {'full_name': full_name},
        data = json.dumps({
            'name':'web',
            'active': True,
            'events': ['push'],
            'config': {
                'url': HOOK_URL,
                'content_type': 'json',
                'secret': '11' # TODO: sign from name and SECRET.
            }
         })
    )
    if resp.status_code < 300: # no errors, in 2xx range
        project = Project.query.filter_by(login = g.user.login, full_name = full_name).first()
        if not project:
            project = Project(
                login = g.user.login,
                full_name = full_name,
                clone = 'git://github.com/%s.git' % full_name,
                is_github = True
            )
        project_data = auth.get('/repos/%s' % full_name)
        if project_data.status_code == 200:
            project.cache_update(data = project_data.json())
        else:
            flash(_('Repository information update error'))
            return redirect(url_for('settings.repos'))
        project.is_github = True
        db.session.add(project)
        db.session.commit()
    else:
        logging.error('Web hook registration error for %s' % full_name)
        flash(_('Repository webhook update error'))
        return redirect(url_for('settings.repos'))

    flash(_('Added webhook for %s.' % (full_name)))
    git_clone(login = g.user.login, project_id = project.id, clone = project.clone)
    return redirect(url_for('settings.repos')+"#tab_github")

@login_required
@settings.route('/delhook/<path:full_name>', methods=['GET'])
def delhook(full_name):
    auth = github.get_session(token = session['token'])

    old_hooks = auth.get('/repos/%s/hooks' % full_name)
    if old_hooks.status_code != 200:
        logging.error('Repos API reading error for user %s' % g.user.login)
        flash(_('GitHub API access error, please try again later'))
        return redirect(url_for('settings.repos')+"#tab_github")

    exist_id = False
    if old_hooks.json():
        for i in old_hooks.json():
            if i.has_key('name') and i['name'] == 'web':
                if i.has_key('config') and i['config'].has_key('url') \
                    and i['config']['url'] == HOOK_URL:
                    exist_id = i['id']

    if exist_id:
        resp = auth.delete('/repos/%(full_name)s/hooks/%(id)s' % {'full_name': full_name, 'id': exist_id})
        if resp.status_code != 204:
            flash(_('Error deleting old webhook, delete if manually or retry'))
    else:
        flash(_("Webhook is not registered on github, probably it was deleted manually"))

    project = Project.query.filter_by(login = g.user.login, full_name = full_name).first()

    if project:
        db.session.delete(project)
        db.session.commit()

    git_clean(login = g.user.login, project_id = project.id)
    return redirect(url_for('settings.repos')+"#tab_github")

@login_required
@settings.route('/addclone', methods=['POST'])
def addclone():
    clone = request.form.get('clone')
    dup = Project.query.filter_by(login = g.user.login, is_github=False, clone = clone).first()
    if dup:
        flash(_("Repository already added"))
        return redirect(url_for('settings.repos')+"#tab_owngit")

    project = Project(
        login = g.user.login,
        clone = clone,
        is_github = False)

    if project:
        db.session.add(project)
        db.session.commit()

    flash(Markup(_("Repository successfully added to <a href='/'>the list</a>")))
    git_clone(login = g.user.login, project_id = project.id, clone = project.clone)
    return redirect(url_for('settings.repos')+"#tab_owngit")

@login_required
@settings.route('/delclone/', methods=['GET'])
def delclone():
    project_id = request.args.get('project_id')
    project = Project.query.filter_by(login = g.user.login, id = project_id).first()
    if not project:
        flash(_("Cann't find clone sting"))
        return redirect(url_for('settings.repos')+"#tab_owngit")

    db.session.delete(project)
    db.session.commit()
    flash(_("Repository succesfuly deleted"))
    git_clean(login = g.user.login, project_id = project.id)
    return redirect(url_for('settings.repos')+"#tab_owngit")

@login_required
@settings.route('/massgit/', methods=['POST'])
def massgit():
    git_ids = request.form.getlist('git')
    projects = Project.query.filter_by(login = g.user.login, is_github=True).all()

    pfn = {}
    for p in projects:
        if p.full_name not in git_ids:
            git_clean(login = g.user.login, project_id = p.id)
            db.session.delete(p)
            flash(_("Repository %s successfully deleted" % p.full_name))
        pfn[p.full_name] = p

    db.session.commit()
    for gid in git_ids:
        if not pfn.get(gid):
            project = Project(
                login = g.user.login,
                full_name = gid,
                clone = 'git://github.com/%s.git' % gid,
                is_github = True
            )
            db.session.add(project)
            db.session.commit()
            flash(Markup(_("Repository %s successfully added to <a href='/'>the list</a>" % project.full_name)))
            git_clone(login = g.user.login, project_id = project.id, clone = project.clone)

    db.session.commit()
    return redirect(url_for('settings.repos')+"#tab_massgithub")

