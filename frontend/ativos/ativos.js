			/* ═══════ ATIVOS ═══════ */

			async function carregarAtivos() {
				try {
					const ativos = await apiFetch('/ativos');
					renderAtivos(ativos);
					renderStats(ativos);
				} catch (e) {
					toast(e.message, 'error');
				}
			}

			function renderStats(ativos) {
				const count = (s) => ativos.filter((a) => a.status === s).length;
				const cards = [
					{ label: 'Total', value: ativos.length, color: '#e8ecf4' },
					{ label: 'Disponíveis', value: count('DISPONIVEL'), color: '#00e676' },
					{ label: 'Em Uso', value: count('EM_USO'), color: '#4d9fff' },
					{ label: 'Manutenção', value: count('MANUTENCAO'), color: '#ffd166' },
					{ label: 'Descarte', value: count('DESCARTE'), color: '#ff4d6d' },
				];
				document.getElementById('stats-ativos').innerHTML = cards
					.map(
						(c) => `
      <div class="stat-card" style="--glow-color:${c.color}">
        <div class="stat-label">${c.label}</div>
        <div class="stat-value">${c.value}</div>
      </div>
    `,
					)
					.join('');
			}

			function renderAtivos(lista) {
				const tbody = document.getElementById('tbody-ativos');
				if (!lista.length) {
					tbody.innerHTML =
						'<tr><td colspan="6" class="empty">Nenhum ativo encontrado.</td></tr>';
					return;
				}
				tbody.innerHTML = lista
					.map(
						(a) => `
      <tr>
        <td><code style="color:var(--accent);font-size:.8rem">#${a.codigo_ativo}</code></td>
        <td><strong>${a.nome}</strong></td>
        <td class="muted">${a.descricao || '—'}</td>
        <td>${statusBadge(a.status)}</td>
        <td>${a.colaborador ? a.colaborador.nome : '<span style="color:var(--muted)">—</span>'}</td>
        <td>
          <div class="action-group">
            ${
				a.status === 'DISPONIVEL' ?
					`<button class="btn btn-sm btn-green" onclick="abrirEntrega(${a.codigo_ativo},'${esc(a.nome)}')">Entregar</button>`
				:	''
			}
            ${
				a.status === 'MANUTENCAO' ?
					`<button class="btn btn-sm btn-green" onclick="registrarDevolucaoRapida(${a.codigo_ativo}, 'DISPONIVEL')">Concluir Manutenção</button>`
				:	''
			}
            ${
				a.status === 'EM_USO' ?
					`<button class="btn btn-sm btn-yellow" onclick="abrirDevolucao(${a.codigo_ativo},'${esc(a.nome)}')">Devolver</button>`
				:	''
			}
          </div>
        </td>
      </tr>
    `,
					)
					.join('');
			}

			async function buscarAtivos() {
				const termo = document.getElementById('busca-ativo-input').value.trim();
				if (!termo) {
					carregarAtivos();
					return;
				}
				try {
					const res = await apiFetch('/ativos/busca', {
						method: 'POST',
						body: JSON.stringify({ termo }),
					});
					renderAtivos(Array.isArray(res) ? res : [res]);
				} catch (e) {
					toast(e.message, 'error');
				}
			}

			async function criarAtivo() {
				const codigo_ativo = parseInt(document.getElementById('na-codigo').value);
				const nome = document.getElementById('na-nome').value.trim();
				const descricao = document.getElementById('na-desc').value.trim();
				if (!codigo_ativo || !nome || !descricao) {
					toast('Preencha todos os campos', 'error');
					return;
				}
				try {
					await apiFetch('/ativos', {
						method: 'POST',
						body: JSON.stringify({ codigo_ativo, nome, descricao }),
					});
					toast('Ativo criado com sucesso!', 'success');
					closeModal('modal-novo-ativo');
					['na-codigo', 'na-nome', 'na-desc'].forEach(
						(id) => (document.getElementById(id).value = ''),
					);
					carregarAtivos();
				} catch (e) {
					toast(e.message, 'error');
				}
			}

			function abrirEntrega(codigo, nome) {
				document.getElementById('entrega-codigo').value = codigo;
				document.getElementById('entrega-info').textContent = `Ativo: ${nome} (#${codigo})`;
				document.getElementById('entrega-colab').value = '';
				openModal('modal-entrega');
			}

			async function registrarEntrega() {
				const codigo_ativo = parseInt(document.getElementById('entrega-codigo').value);
				const colaborador_id = parseInt(document.getElementById('entrega-colab').value);
				if (!colaborador_id) {
					toast('Informe o ID do colaborador', 'error');
					return;
				}
				try {
					await apiFetch('/entrega', {
						method: 'POST',
						body: JSON.stringify({ codigo_ativo, colaborador_id }),
					});
					toast('Entrega registrada com sucesso!', 'success');
					closeModal('modal-entrega');
					carregarAtivos();
				} catch (e) {
					toast(e.message, 'error');
				}
			}

			async function registrarDevolucaoRapida(codigo_ativo, novo_status) {
				try {
					await apiFetch('/devolucao', {
						method: 'POST',
						body: JSON.stringify({ codigo_ativo, status: novo_status }),
					});
					toast('Manutenção finalizada! Ativo disponível.', 'success');
					carregarAtivos();
				} catch (e) {
					toast(e.message, 'error');
				}
			}

			function abrirDevolucao(codigo, nome) {
				document.getElementById('dev-codigo').value = codigo;
				document.getElementById('dev-info').textContent = `Ativo: ${nome} (#${codigo})`;
				openModal('modal-devolucao');
			}

			async function registrarDevolucao() {
				const codigo_ativo = parseInt(document.getElementById('dev-codigo').value);
				const status = document.getElementById('dev-status').value;
				try {
					await apiFetch('/devolucao', {
						method: 'POST',
						body: JSON.stringify({ codigo_ativo, status }),
					});
					toast('Devolução registrada com sucesso!', 'success');
					closeModal('modal-devolucao');
					carregarAtivos();
				} catch (e) {
					toast(e.message, 'error');
				}
			}
