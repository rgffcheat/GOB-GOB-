"""Pages for Bot Make. install(T, _P) is called from templates_ui2.py before the admin menu is turned into the hamburger drawer."""

BOT_ICON = ('<rect width="18" height="10" x="3" y="11" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/>'
            '<line x1="8" x2="8" y1="16" y2="16"/><line x1="16" x2="16" y1="16" y2="16"/>')

RESELLER_PAGE = r"""{% extends 'rbase.html' %}{% block c %}
<div class=hd>{{ic('bot',24)}} BOT MAKE</div>
{% if mine %}
<div class=card><h3>{{ic('bot',20)}} Your bot</h3>
<table>
<tr><td class=mu>Name</td><td><b>{{mine.bot_name}}</b></td></tr>
<tr><td class=mu>Bot</td><td>{% if mine.bot_username %}<a href="https://t.me/{{mine.bot_username}}" target=_blank rel=noopener>@{{mine.bot_username}}</a>{% else %}-{% endif %}</td></tr>
<tr><td class=mu>Status</td><td>
{% if state=='running' %}<span class="pill a">Running</span>
{% elif state=='starting' %}<span class="pill c">Starting...</span>
{% elif state=='stopped' %}<span class="pill e">Stopped by admin</span>
{% elif state=='expired' %}<span class="pill e">Subscription expired</span>
{% else %}<span class="pill c">Restarting...</span>{% endif %}</td></tr>
<tr><td class=mu>Your admin ID</td><td><code>{{mine.admin_id}}</code></td></tr>
<tr><td class=mu>Created</td><td>{{mine.created|dt}}</td></tr>
<tr><td class=mu>Plan</td><td>{{mine['plan_name'] or 'Legacy'}}</td></tr>
<tr><td class=mu>Expires</td><td>{{mine['expires_at']|dt if mine['expires_at'] else 'No expiry'}}</td></tr>
</table>
<div class=mu style="margin-top:12px">Open your bot in Telegram and send <b>/admin</b> from the admin account. Use your separate Admin Panel link below to manage the bot website.</div>
<div class=hint style="margin-top:10px">Admin Panel: <a href="/bot-admin/{{mine.instance_id}}/login" target=_blank rel=noopener>Open Bot Admin Panel</a><br>Username: <code>{{panel_user}}</code><br>Password: <code>{{panel_pass}}</code></div>
{% if state in ('starting','down','gaveup') %}<script>setTimeout(function(){(window.rgReload?rgReload():location.reload())},6000)</script>{% endif %}
</div>
{% elif full %}
<div class=card><div class=hint>Bot creation is full right now. Please contact the admin.</div></div>
{% else %}
<div class=card><h3>{{ic('plus',20)}} Create your own bot</h3>
<div class=mu>Choose a subscription using your reseller wallet. Make a bot in <b>@BotFather</b> first, then fill the details. Your bot will start automatically after validation.</div>
<form method=post id=bmf style="margin-top:12px">
<p class=mu style="margin:14px 0 4px">Subscription Plan</p>
<select name=plan_id required style="width:100%"><option value="">Choose a plan</option>{% for p in plans %}<option value="{{p.id}}">{{p.name}} · {{p.days}} day(s) · ₹{{'%.2f'|format(p.price)}}</option>{% endfor %}</select>
<p class=mu style="margin:14px 0 4px">Bot name <span class=mu>(shown everywhere inside the bot)</span></p>
<input name=name maxlength=40 required placeholder="e.g. My Cheat Shop" style="width:100%" autocomplete=off>
<p class=mu style="margin:14px 0 4px">Bot API token <span class=mu>(from @BotFather)</span></p>
<input name=token required placeholder="123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" style="width:100%" autocomplete=off autocapitalize=off spellcheck=false>
<p class=mu style="margin:14px 0 4px">Admin ID <span class=mu>(your Telegram numeric ID - this account becomes the bot's admin)</span></p>
<input name=admin_id required inputmode=numeric pattern="[0-9]{5,15}" placeholder="e.g. 123456789" style="width:100%" autocomplete=off>
<button class=genb id=bmb style="margin-top:18px">{{ic('bot',20)}} CREATE BOT</button>
</form>
<script>document.getElementById('bmf').onsubmit=function(){var b=document.getElementById('bmb');b.disabled=true;b.textContent='Creating... please wait';return true}</script>
</div>
{% endif %}
{% endblock %}"""

ADMIN_PAGE = r"""{% extends 'abase.html' %}{% block c %}<h2>{{ic('bot',24)}} Reseller Bots</h2>
{% if not template_ok %}<div class="flash err">RGG Bot v21 package is missing from this deployment. No new bot can start until it is restored.</div>{% endif %}
<div class=card><h3>Bot code {% if template_ok %}<span class="pill a">Ready</span>{% else %}<span class="pill e">Missing</span>{% endif %}</h3>
<div class=mu>{% if template_ok %}Bundled source: {{template_info}}. Every bot gets a private copy of all RGG Bot v21 modules and an isolated SQLite database.{% endif %}</div>
<div class=row style="margin-top:10px"><a href="/admin/bots/plans"><button type=button class=o>Subscription Plans &amp; Backup Settings</button></a></div>
<form method=post action="/admin/bots/restart-all" style="margin-top:10px" onsubmit="return confirm('Restart every running bot now?')"><button class=o>Restart all bots (apply new code)</button></form></div>
<div class=card>
<div class=mu>Every bot also gets your admin ID <code>{{owner or 'not set'}}</code> (set in Admin &gt; Telegram) - it is always an admin and cannot be removed inside the bot.</div>
<form method=post class=row style="margin-top:10px"><input type=hidden name=action value=max>
<span class=mu>Max bots allowed:</span><input name=max value="{{maxb}}" inputmode=numeric style="width:90px"><button class=g>Save</button></form>
<div class=row style="margin-top:12px;gap:10px;flex-wrap:wrap">
<a href="/admin/bots/backup"><button type=button class=o>{{ic('save',16)}} Backup all bots (.zip)</button></a>
<form method=post action="/admin/bots/restore" enctype=multipart/form-data class=row style="gap:8px"><input type=file name=file accept=".zip" required><button class=o onclick="return confirm('Restore bots from this backup?')">Restore</button></form></div>
<div class=mu style="margin-top:8px">Render free disk is wiped on every redeploy: download the bots backup after changes and restore it after a redeploy. The backup file contains bot tokens - keep it private.</div>
</div>
{% for b in rows %}{% set s=states[b.instance_id] %}
<div class=card>
<div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center">
<div><b style="font-size:17px">{{b.bot_name}}</b>{% if b.bot_username %} &nbsp;<a href="https://t.me/{{b.bot_username}}" target=_blank rel=noopener>@{{b.bot_username}}</a>{% endif %}
<div class=mu>Reseller: <b>{{b.reseller_name or '-'}}</b> &middot; Admin ID: <code>{{b.admin_id}}</code> &middot; token ...{{b.token_tail}} &middot; plan {{b.plan_name or 'Legacy'}} &middot; expires {{b.expires_at|dt if b.expires_at else 'Never'}} &middot; made {{b.created|dt}}</div><div class=mu><a href="/bot-admin/{{b.instance_id}}/login" target=_blank rel=noopener>Open this bot's Admin Panel</a></div></div>
<div>{% if s=='running' %}<span class="pill a">Running</span>{% elif s=='starting' %}<span class="pill c">Starting</span>{% elif s=='stopped' %}<span class="pill e">Stopped</span>{% elif s=='expired' %}<span class="pill e">Expired</span>{% elif s=='gaveup' %}<span class="pill e">Crashing</span>{% else %}<span class="pill c">Restarting</span>{% endif %}</div></div>
{% if b.note %}<div class=hint style="margin-top:8px">{{b.note}}</div>{% endif %}
<div class=row style="margin-top:12px;gap:8px;flex-wrap:wrap">
{% if b.desired=='stopped' %}<form method=post action="/admin/bots/{{b.instance_id}}/start"><button class=g>Start</button></form>
{% else %}<form method=post action="/admin/bots/{{b.instance_id}}/stop" onsubmit="return confirm('Stop this bot?')"><button class=r>Stop</button></form>{% endif %}
<form method=post action="/admin/bots/{{b.instance_id}}/restart"><button class=o>Restart</button></form>
<a href="/admin/bots/{{b.instance_id}}/log" target=_blank><button type=button class=o>Log</button></a>
<a href="/admin/bots/{{b.instance_id}}/db.download"><button type=button class=o>{{ic('save',16)}} Database</button></a>
<a href="/admin/bots/{{b.instance_id}}/backup"><button type=button class=o>Backup Bot</button></a>
<form method=post action="/admin/bots/{{b.instance_id}}/delete" onsubmit="return confirm('DELETE this bot and its whole database? This cannot be undone.')"><button class=r>{{ic('trash',16)}} Delete</button></form></div>
<form method=post action="/admin/bots/{{b.instance_id}}/db" enctype=multipart/form-data class=row style="margin-top:10px;gap:8px;flex-wrap:wrap" onsubmit="return confirm('Replace this bot database with the uploaded one? The bot restarts. A safety copy of the old database is kept.')">
<span class=mu>Add / restore database (.db or .zip):</span><input type=file name=file accept=".db,.sqlite,.sqlite3,.zip" required><button class=o>Upload</button></form>
</div>
{% else %}<div class=card><span class=mu>No reseller has made a bot yet.</span></div>{% endfor %}
{% endblock %}"""


def install(T, _P):
    _P["bot"] = BOT_ICON
    T["bot_make.html"] = RESELLER_PAGE
    T["admin_bots.html"] = ADMIN_PAGE
    T["admin_bot_plans.html"] = r"""{% extends 'abase.html' %}{% block c %}<h2>Bot Maker · Plans &amp; Backup</h2>
<div class=card><h3>Create subscription plan</h3><form method=post><input type=hidden name=action value=save>
<label>Plan name</label><input name=name maxlength=40 required placeholder="e.g. 7 Days Premium">
<label>Duration (days)</label><input name=days type=number min=1 max=36500 required>
<label>Price (₹)</label><input name=price type=number min=0 step=0.01 required>
<button class=g>Add Plan</button></form></div>
<div class=card><h3>Telegram backup destination</h3><form method=post><input type=hidden name=action value=backup_chat>
<label>Telegram Chat ID</label><input name=chat_id value="{{backup_chat}}" placeholder="e.g. 123456789">
<label>Automatic backup interval (hours)</label><input name=hours type=number min=1 max=168 value="{{backup_hours}}" required>
<button class=g>Save Backup Settings</button></form><div class=mu>Uses the website's configured Telegram bot token to send the full bots ZIP automatically at the selected interval and when you manually back up all bots.</div></div>
<div class=card><h3>Available plans</h3><div class=mu>Set each plan's name, duration and wallet price before switching it ON. Starter examples are OFF until configured.</div>{% for p in plans %}<form method=post class=row style="gap:8px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding:10px 0"><input type=hidden name=id value={{p.id}}><input type=hidden name=action value=update><input name=name value="{{p.name}}" required style="flex:2;min-width:120px"><input name=days type=number min=1 value={{p.days}} required style="width:85px"><input name=price type=number min=0 step=0.01 value="{{'%.2f'|format(p.price)}}" required style="width:100px"><button class=o>Save</button></form><div class=row style="gap:8px;margin:0 0 10px"><span class=mu>{{'Active' if p.active else 'OFF'}} · ₹{{'%.2f'|format(p.price)}} / {{p.days}} day(s)</span><form method=post><input type=hidden name=action value=toggle><input type=hidden name=id value={{p.id}}><button class=o>Turn {{'OFF' if p.active else 'ON'}}</button></form><form method=post onsubmit="return confirm('Delete this plan?')"><input type=hidden name=action value=delete><input type=hidden name=id value={{p.id}}><button class=r>Delete</button></form></div>{% else %}<div class=mu>No plans yet.</div>{% endfor %}</div>{% endblock %}"""
    link = '{% if bm_allowed(request.r) %}<a href="/bot-make" class="{{\'on\' if page==\'botmake\'}}">{{ic(\'bot\')}} Bot Make</a>{% endif %}\n<a href="/security"'
    assert '<a href="/security"' in T["rbase.html"]
    T["rbase.html"] = T["rbase.html"].replace('<a href="/security"', link, 1)       # directly above Security
    alink = '<a href="/admin/bots" class="{{\'on\' if page==\'bots\'}}">Bots</a><a href="/admin/bots/plans">Bot Plans</a><a href="/admin/gateway"'
    assert '<a href="/admin/gateway"' in T["abase.html"]
    T["abase.html"] = T["abase.html"].replace('<a href="/admin/gateway"', alink, 1)
