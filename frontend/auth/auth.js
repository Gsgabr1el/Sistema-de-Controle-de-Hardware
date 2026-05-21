			/* ═══════ AUTH ═══════ */

			async function doLogin() {
				const username = document.getElementById('login-user').value.trim();
				const senha = document.getElementById('login-pass').value;
				const errEl = document.getElementById('login-err');
				errEl.style.display = 'none';

				try {
					const res = await fetch(API + '/login', {
						method: 'POST',
						headers: { 'Content-Type': 'application/json' },
						body: JSON.stringify({ username, senha }),
					});
					const data = await res.json();
					if (!data.access_token) throw new Error(data.detail || 'Credenciais inválidas');

					TOKEN = data.access_token;
					localStorage.setItem('hw_token', TOKEN);
					document.getElementById('header-user').textContent = username;

					document.getElementById('login-screen').style.display = 'none';
					document.getElementById('app').style.display = 'flex';
					carregarAtivos();
				} catch (e) {
					errEl.textContent = e.message;
					errEl.style.display = 'block';
				}
			}

			function doLogout() {
				TOKEN = '';
				localStorage.removeItem('hw_token');
				document.getElementById('login-screen').style.display = 'flex';
				document.getElementById('app').style.display = 'none';
			}
