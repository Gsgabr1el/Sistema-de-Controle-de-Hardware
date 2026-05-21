			/* ═══════ MOVIMENTAÇÕES ═══════ */

			async function carregarMovimentacoes() {
				try {
					const lista = await apiFetch('/movimentacoes');
					const tbody = document.getElementById('tbody-movs');
					if (!lista.length) {
						tbody.innerHTML =
							'<tr><td colspan="5" class="empty">Nenhuma movimentação registrada.</td></tr>';
						return;
					}
					tbody.innerHTML = [...lista]
						.reverse()
						.map(
							(m) => `
        <tr>
          <td class="muted" style="font-size:.78rem">#${m.id}</td>
          <td class="muted" style="font-size:.84rem">${fmtDate(m.data_hora)}</td>
          <td>${tipoBadge(m.tipo)}</td>
          <td>
            <code style="color:var(--accent);font-size:.78rem">#${m.codigo_ativo}</code>
            ${m.ativo ? `<span style="color:var(--muted2);margin-left:6px;font-size:.84rem">${m.ativo.nome}</span>` : ''}
          </td>
          <td>${m.colaborador ? m.colaborador.nome : '<span style="color:var(--muted)">—</span>'}</td>
        </tr>
      `,
						)
						.join('');
				} catch (e) {
					toast(e.message, 'error');
				}
			}
