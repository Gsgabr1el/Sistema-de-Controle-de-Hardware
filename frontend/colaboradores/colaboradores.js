			/* ═══════ COLABORADORES ═══════ */

			async function carregarColaboradores() {
				try {
					const lista = await apiFetch('/colaboradores');
					renderColabs(lista);
				} catch (e) {
					toast(e.message, 'error');
				}
			}

			function renderColabs(lista) {
				const tbody = document.getElementById('tbody-colabs');
				if (!lista || !lista.length) {
					tbody.innerHTML =
						'<tr><td colspan="6" class="empty">Nenhum colaborador encontrado.</td></tr>';
					return;
				}
				tbody.innerHTML = lista
					.map(
						(c) => `
      <tr>
        <td><code style="color:var(--accent);font-size:.8rem">${c.id}</code></td>
        <td><strong>${c.nome}</strong></td>
        <td class="muted">${c.email || '—'}</td>
        <td>${c.departamento ? `<span class="badge badge-blue">${c.departamento}</span>` : '<span style="color:var(--muted)">—</span>'}</td>
        <td>
          ${
				c.ativos && c.ativos.length > 0 ?
					c.ativos
						.map(
							(a) =>
								`<div style="font-size:.75rem;margin-bottom:2px"><code style="color:var(--accent)">#${a.codigo_ativo}</code> ${a.nome}</div>`,
						)
						.join('')
				:	'<span style="color:var(--muted);font-size:.75rem">Nenhum</span>'
			}
        </td>
        <td>
          <div class="action-group">
            <button class="btn btn-sm btn-ghost" onclick="abrirEditarColaborador(${c.id}, '${esc(c.nome)}', '${esc(c.email)}', '${esc(c.departamento)}')">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
            </button>
            <button class="btn btn-sm btn-red" onclick="excluirColaborador(${c.id}, '${esc(c.nome)}')">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
            </button>
          </div>
        </td>
      </tr>
    `,
					)
					.join('');
			}

			async function criarColaborador() {
				const nome = document.getElementById('nc-nome').value.trim();
				const email = document.getElementById('nc-email').value.trim();
				const departamento = document.getElementById('nc-depto').value.trim();

				if (!nome || !email || !departamento) {
					toast('Preencha todos os campos', 'error');
					return;
				}

				try {
					await apiFetch('/colaboradores', {
						method: 'POST',
						body: JSON.stringify({ nome, email, departamento }),
					});
					toast('Colaborador cadastrado com sucesso!', 'success');
					closeModal('modal-novo-colab');
					['nc-nome', 'nc-email', 'nc-depto'].forEach((id) => (document.getElementById(id).value = ''));
					carregarColaboradores();
				} catch (e) {
					toast(e.message, 'error');
				}
			}

			function abrirEditarColaborador(id, nome, email, depto) {
				document.getElementById('ec-id').value = id;
				document.getElementById('ec-nome').value = nome;
				document.getElementById('ec-email').value = email;
				document.getElementById('ec-depto').value = depto;
				openModal('modal-edit-colab');
			}

			async function salvarEdicaoColaborador() {
				const id = document.getElementById('ec-id').value;
				const nome = document.getElementById('ec-nome').value.trim();
				const email = document.getElementById('ec-email').value.trim();
				const departamento = document.getElementById('ec-depto').value.trim();

				try {
					await apiFetch(`/colaboradores/${id}`, {
						method: 'PUT',
						body: JSON.stringify({ nome, email, departamento }),
					});
					toast('Colaborador atualizado!', 'success');
					closeModal('modal-edit-colab');
					carregarColaboradores();
				} catch (e) {
					toast(e.message, 'error');
				}
			}

			async function excluirColaborador(id, nome) {
				if (!confirm(`Deseja realmente excluir o colaborador "${nome}"?`)) return;

				try {
					await apiFetch(`/colaboradores/${id}`, { method: 'DELETE' });
					toast('Colaborador removido!', 'success');
					carregarColaboradores();
				} catch (e) {
					toast(e.message, 'error'); // Aqui será exibido o erro da Opção A se houver ativos.
				}
			}

			async function buscarColaborador() {
				const id = parseInt(document.getElementById('busca-colab-input').value);
				if (!id) {
					carregarColaboradores();
					return;
				}
				try {
					const c = await apiFetch('/colaboradores/busca', {
						method: 'POST',
						body: JSON.stringify({ colaborador_id: id }),
					});
					renderColabs([c]);
				} catch (e) {
					toast(e.message, 'error');
				}
			}
