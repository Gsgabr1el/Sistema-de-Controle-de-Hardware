			// Auto-login
			(async () => {
				if (!TOKEN) return;
				try {
					await apiFetch('/ativos');
					document.getElementById('login-screen').style.display = 'none';
					document.getElementById('app').style.display = 'flex';
					carregarAtivos();
				} catch {
					TOKEN = '';
					localStorage.removeItem('hw_token');
				}
			})();

			document.addEventListener('keydown', (e) => {
				if (
					e.key === 'Enter' &&
					document.getElementById('login-screen').style.display !== 'none'
				)
					doLogin();
			});
			/* ═══════ MODAL CLOSE ON OVERLAY ═══════ */
			document.querySelectorAll('.modal-overlay').forEach((el) => {
				el.addEventListener('click', (e) => {
					if (e.target === el) el.classList.remove('open');
				});
			});
