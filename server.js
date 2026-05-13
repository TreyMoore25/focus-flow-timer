const express = require('express');
const session = require('express-session');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

const ALLOWED_EMAIL = 'treym1508@gmail.com';
const LOGIN_PASSWORD = process.env.LOGIN_PASSWORD;
const SESSION_SECRET = process.env.SESSION_SECRET || 'fallback-secret-change-in-railway';

app.use(express.urlencoded({ extended: true }));
app.use(session({
  secret: SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: { maxAge: 24 * 60 * 60 * 1000 }
}));

function requireAuth(req, res, next) {
  if (req.session.authenticated) return next();
  res.redirect('/login');
}

const loginPage = (error = '') => `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Focus Flow — Login</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #0f0f1a;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      color: #e0e0f0;
    }
    .card {
      background: #1a1a2e;
      border: 1px solid #2a2a4a;
      border-radius: 16px;
      padding: 40px 48px;
      width: 100%;
      max-width: 400px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    h1 {
      font-size: 1.6rem;
      font-weight: 700;
      margin-bottom: 6px;
      color: #c084fc;
    }
    p.subtitle {
      font-size: 0.85rem;
      color: #6b6b8a;
      margin-bottom: 28px;
    }
    label {
      display: block;
      font-size: 0.8rem;
      font-weight: 600;
      color: #9090b0;
      margin-bottom: 6px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    input {
      width: 100%;
      padding: 10px 14px;
      background: #0f0f1a;
      border: 1px solid #2a2a4a;
      border-radius: 8px;
      color: #e0e0f0;
      font-size: 0.95rem;
      margin-bottom: 18px;
      outline: none;
      transition: border-color 0.2s;
    }
    input:focus { border-color: #c084fc; }
    button {
      width: 100%;
      padding: 11px;
      background: #7c3aed;
      color: #fff;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s;
    }
    button:hover { background: #6d28d9; }
    .error {
      background: #3b1a1a;
      border: 1px solid #7f1d1d;
      color: #fca5a5;
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 0.85rem;
      margin-bottom: 18px;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>Focus Flow</h1>
    <p class="subtitle">Sign in to access your timer</p>
    ${error ? `<div class="error">${error}</div>` : ''}
    <form method="POST" action="/login">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" placeholder="you@example.com" required autocomplete="email" />
      <label for="password">Password</label>
      <input type="password" id="password" name="password" placeholder="••••••••" required autocomplete="current-password" />
      <button type="submit">Sign In</button>
    </form>
  </div>
</body>
</html>
`;

app.get('/login', (req, res) => {
  if (req.session.authenticated) return res.redirect('/');
  res.send(loginPage());
});

app.post('/login', (req, res) => {
  const email = (req.body.email || '').toLowerCase().trim();
  const password = req.body.password || '';

  if (email === ALLOWED_EMAIL && password === LOGIN_PASSWORD) {
    req.session.authenticated = true;
    return res.redirect('/');
  }

  res.send(loginPage('Incorrect email or password.'));
});

app.get('/logout', (req, res) => {
  req.session.destroy(() => res.redirect('/login'));
});

app.get('/', requireAuth, (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
