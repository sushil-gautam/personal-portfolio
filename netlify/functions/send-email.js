// Netlify Function: send-email
// Sends contact form data to Gmail via SMTP using environment variables.

const nodemailer = require('nodemailer');

exports.handler = async function(event, context) {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method Not Allowed' })
    };
  }

  // Parse URL‑encoded form data
  const contentType = event.headers['content-type'] || '';
  let name = '';
  let email = '';
  let message = '';
  if (contentType.includes('application/json')) {
    const data = JSON.parse(event.body);
    name = data.name || '';
    email = data.email || '';
    message = data.message || '';
  } else {
    const params = new URLSearchParams(event.body);
    name = params.get('name') || '';
    email = params.get('email') || '';
    message = params.get('message') || '';
  }

  const gmailUser = process.env.GMAIL_USER;
  const gmailPass = process.env.GMAIL_PASS;

  if (!gmailUser || !gmailPass) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Server email configuration missing.' })
    };
  }

  const transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 587,
    secure: false,
    auth: {
      user: gmailUser,
      pass: gmailPass
    }
  });

  const mailOptions = {
    from: gmailUser,
    to: gmailUser,
    subject: `Portfolio Contact from ${name}`,
    text: `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`
  };

  try {
    await transporter.sendMail(mailOptions);
    return {
      statusCode: 200,
      body: JSON.stringify({ status: 'success' })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
