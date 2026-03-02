<svelte:head>
<meta charset="UTF-8">
  <title>Verify your email · Kiadez</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      background-color: #0e1a14;
      font-family: Arial, Helvetica, sans-serif;
      color: #1e1e1e;
    }
  </style>
</svelte:head>

<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0e1a14; padding:40px 0;">
  <tbody>
    <tr>
      <td align="center">

        <table width="600" cellpadding="0" cellspacing="0" style="
          background:#ffffff;
          border-radius:12px;
          overflow:hidden;
        ">
          <tbody>
            <!-- Header -->
            <tr>
              <td align="center" style="
                background:#00674F;
                padding:30px;
              ">
                <img src="https://kiadez.com/assets/logo-email.png" alt="Kiadez" width="120" style="display:block;" />
              </td>
            </tr>

            <!-- Body -->
            <tr>
              <td style="padding:35px;">
                <h2 style="text-align:center; margin-top:0; color:#1e1e1e;">
                  Welcome to Kiadez
                </h2>

                <p style="text-align:center; font-size:15px; line-height:1.6;">
                  Thank you for signing up to <strong>Kiadez</strong>.
                  To continue and activate your account, confirm your email address.
                </p>

                <div style="text-align:center; margin:30px 0;">
                  <a href="{verify_url}" style="
                       display:inline-block;
                       padding:14px 28px;
                       background:#00674F;
                       color:#ffffff;
                       text-decoration:none;
                       border-radius:8px;
                       font-weight:bold;
                       font-size:15px;
                     ">
                    Verify email
                  </a>
                </div>

                <p style="text-align:center; font-size:14px; color:#555;">
                  If you did not request this account, you can ignore this message.
                </p>

                <hr style="border:none; border-top:1px solid #e0e0e0; margin:30px 0;">

                <p style="font-size:12px; color:#777; text-align:center;">
                  Kiadez · Consciousness Engineering<br>
                  A social network to fulfill wishes
                </p>
              </td>
            </tr>
          </tbody>
        </table>

      </td>
    </tr>
  </tbody>
</table>
