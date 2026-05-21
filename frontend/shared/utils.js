			const API = window.location.origin;
			let TOKEN = localStorage.getItem('hw_token') || '';

			/* ═══════ UTILS ═══════ */

			function toast(msg, type = 'info') {
				const el = document.createElement('div');
				el.className = `toast ${type}`;
				el.innerHTML = `<div class="toast-dot"></div><span>${msg}</span>`;
				document.getElementById('toast-container').appendChild(el);
				setTimeout(() => {
					el.style.opacity = '0';
					el.style.transform = 'translateY(8px)';
					el.style.transition = '.2s';
					setTimeout(() => el.remove(), 200);
				}, 3200);
			}

			function openModal(id) {
				document.getElementById(id).classList.add('open');
			}
			function closeModal(id) {
				document.getElementById(id).classList.remove('open');
			}

			function showPage(name, btn) {
				document.querySelectorAll('.page').forEach((p) => p.classList.remove('active'));
				document.querySelectorAll('.nav-tab').forEach((b) => b.classList.remove('active'));
				document.getElementById('page-' + name).classList.add('active');
				btn.classList.add('active');
				if (name === 'ativos') carregarAtivos();
				if (name === 'colaboradores') carregarColaboradores();
				if (name === 'movimentacoes') carregarMovimentacoes();
			}

			async function apiFetch(path, opts = {}) {
				const res = await fetch(API + path, {
					headers: {
						'Content-Type': 'application/json',
						Authorization: 'Bearer ' + TOKEN,
					},
					...opts,
				});
				if (res.status === 401) {
					doLogout();
					throw new Error('Sessão expirada');
				}
				const data = await res.json().catch(() => ({}));
				if (!res.ok) throw new Error(data.detail || 'Erro na requisição');
				return data;
			}

			function statusBadge(s) {
				const map = {
					DISPONIVEL: ['badge-green', 'Disponível'],
					EM_USO: ['badge-blue', 'Em Uso'],
					MANUTENCAO: ['badge-yellow', 'Manutenção'],
					DESCARTE: ['badge-red', 'Descarte'],
				};
				const [cls, label] = map[s] || ['badge-green', s];
				return `<span class="badge ${cls}">${label}</span>`;
			}

			function tipoBadge(t) {
				const map = {
					ENTREGA: ['badge-blue', 'Entrega'],
					DEVOLUCAO: ['badge-green', 'Devolução'],
					MANUTENCAO: ['badge-yellow', 'Manutenção'],
					DESCARTE: ['badge-red', 'Descarte'],
				};
				const [cls, label] = map[t] || ['badge-green', t];
				return `<span class="badge ${cls}">${label}</span>`;
			}

			function fmtDate(d) {
				if (!d) return '—';
				return new Date(d).toLocaleString('pt-BR', {
					day: '2-digit',
					month: '2-digit',
					year: 'numeric',
					hour: '2-digit',
					minute: '2-digit',
				});
			}

			function esc(s) {
				return (s || '').replace(/'/g, "\\'").replace(/"/g, '&quot;');
			}
