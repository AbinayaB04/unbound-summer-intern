const apiBase = "http://127.0.0.1:8000";

// COMMANDS
async function submitCommand() {
    const apiKey = document.getElementById("apiKey").value.trim();
    const commandText = document.getElementById("commandText").value.trim();
    const messages = document.getElementById("messages");

    if (!apiKey || !commandText) {
        messages.innerHTML = `<div class="alert alert-warning">API Key and Command required!</div>`;
        return;
    }

    try {
        const res = await fetch(`${apiBase}/commands/`, {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-API-Key": apiKey },
            body: JSON.stringify({ command_text: commandText })
        });
        const data = await res.json();
        messages.innerHTML = `<div class="alert alert-info">${JSON.stringify(data)}</div>`;
        loadCommands(apiKey);
        loadLogs(apiKey);
    } catch(err) {
        console.error(err);
        messages.innerHTML = `<div class="alert alert-danger">Error: ${err}</div>`;
    }
}

async function loadCommands(apiKey) {
    try {
        const res = await fetch(`${apiBase}/commands/`, { headers: { "X-API-Key": apiKey } });
        const commands = await res.json();
        const ul = document.getElementById("commandHistory");
        ul.innerHTML = "";
        commands.forEach(cmd => {
            const li = document.createElement("li");
            li.className = "list-group-item";
            li.textContent = `${cmd.command_text} → ${cmd.status} (Credits used: ${cmd.credits_used})`;
            ul.appendChild(li);
        });
    } catch(err){ console.error(err); }
}

async function loadLogs(apiKey) {
    try {
        const res = await fetch(`${apiBase}/logs/`, { headers: { "X-API-Key": apiKey } });
        if(res.status === 200){
            const logs = await res.json();
            const ul = document.getElementById("logs");
            ul.innerHTML = "";
            logs.forEach(log => {
                const li = document.createElement("li");
                li.className = "list-group-item";
                li.textContent = `User ${log.user_id}: ${log.command_text} → ${log.action}`;
                ul.appendChild(li);
            });
        }
    } catch(err){ console.error(err); }
}

// USERS
async function createUser() {
    const apiKey = document.getElementById("apiKey").value.trim();
    const name = document.getElementById("newUserName").value.trim();
    const role = document.getElementById("newUserRole").value;
    const messages = document.getElementById("messages");

    if (!name || !apiKey) {
        messages.innerHTML = `<div class="alert alert-warning">API Key and User name required!</div>`;
        return;
    }

    try {
        const res = await fetch(`${apiBase}/users/`, {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-API-Key": apiKey },
            body: JSON.stringify({ name: name, role: role })
        });
        const data = await res.json();
        messages.innerHTML = `<div class="alert alert-success">User created: ${JSON.stringify(data)}</div>`;
        loadUsers(apiKey);
    } catch(err) {
        console.error(err);
        messages.innerHTML = `<div class="alert alert-danger">Error: ${err}</div>`;
    }
}

async function loadUsers(apiKey) {
    try {
        const res = await fetch(`${apiBase}/users/`, { headers: { "X-API-Key": apiKey } });
        const users = await res.json();
        const ul = document.getElementById("userList");
        ul.innerHTML = "";
        users.forEach(u => {
            const li = document.createElement("li");
            li.className = "list-group-item";
            li.textContent = `${u.name} → ${u.role} (Credits: ${u.credits})`;
            ul.appendChild(li);
        });
    } catch(err){ console.error(err); }
}

// RULES
async function createRule() {
    const apiKey = document.getElementById("apiKey").value.trim();
    const pattern = document.getElementById("newRulePattern").value.trim();
    const action = document.getElementById("newRuleAction").value;
    const messages = document.getElementById("messages");

    if(!pattern || !apiKey){
        messages.innerHTML = `<div class="alert alert-warning">API Key and Pattern required!</div>`;
        return;
    }

    try {
        const res = await fetch(`${apiBase}/rules/`, {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-API-Key": apiKey },
            body: JSON.stringify({ pattern: pattern, action: action })
        });
        const data = await res.json();
        messages.innerHTML = `<div class="alert alert-success">Rule added: ${JSON.stringify(data)}</div>`;
        loadRules(apiKey);
    } catch(err){
        console.error(err);
        messages.innerHTML = `<div class="alert alert-danger">Error: ${err}</div>`;
    }
}

async function loadRules(apiKey) {
    try {
        const res = await fetch(`${apiBase}/rules/`, { headers: { "X-API-Key": apiKey } });
        const rules = await res.json();
        const ul = document.getElementById("ruleList");
        ul.innerHTML = "";
        rules.forEach(r => {
            const li = document.createElement("li");
            li.className = "list-group-item";
            li.textContent = `${r.pattern} → ${r.action}`;
            ul.appendChild(li);
        });
    } catch(err){ console.error(err); }
}
