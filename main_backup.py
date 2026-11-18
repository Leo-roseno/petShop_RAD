combo_servico.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
combo_servico.set('Consulta')
criar_campo('Data/Horário', 4, 2)
frame_formulario.columnconfigure(1, weight=1)
frame_formulario.columnconfigure(3, weight=1)


def consultar_viacep(cep):
    """Consulta o serviço numa thread e entrega o resultado à interface por uma fila."""
    try:
        url = f'https://viacep.com.br/ws/{cep}/json/'
        with urllib.request.urlopen(url, timeout=5) as resposta:
            dados = json.loads(resposta.read().decode('utf-8'))

        if dados.get('erro'):
            fila_cep.put((cep, None, 'CEP não encontrado.'))
        else:
            fila_cep.put((cep, dados, None))
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as erro:
        fila_cep.put((
            cep, None,
            'Não foi possível consultar o CEP. Verifique sua conexão e tente novamente.'
        ))


def normalizar_cep(valor):
    return valor.strip().replace('-', '').replace('.', '').replace(' ', '')


def buscar_cep():
    cep = normalizar_cep(campos['CEP'].get())
    if len(cep) != 8 or not cep.isdigit():
        registrar_log('CONSULTA CEP', f'CEP "{cep}" rejeitado: formato inválido.')
        messagebox.showwarning('CEP inválido', 'Digite um CEP válido com 8 números.')
        return

    for nome in ['Logradouro', 'Bairro', 'Cidade/UF']:
        campos[nome].delete(0, tk.END)

    botao_cep.config(state='disabled')
    threading.Thread(target=consultar_viacep, args=(cep,), daemon=True).start()


def verificar_respostas_cep():
    try:
        while True:
            cep, dados, erro = fila_cep.get_nowait()
            botao_cep.config(state='normal')

            # O histórico registra a consulta mesmo que o usuário tenha alterado o CEP.
            if erro:
                registrar_log('CONSULTA CEP', f'CEP "{cep}" - {erro}')
            else:
                cidade = dados.get('localidade', '')
                uf = dados.get('uf', '')
                registrar_log(
                    'CONSULTA CEP',
                    f'CEP "{cep}" consultado com sucesso ({cidade}/{uf}).'
                )

            if normalizar_cep(campos['CEP'].get()) != cep:
                continue

            if erro:
                messagebox.showwarning('Consulta ViaCEP', erro)
                continue

            endereco = {
                'Logradouro': dados.get('logradouro', ''),
                'Bairro': dados.get('bairro', ''),
                'Cidade/UF': f"{dados.get('localidade', '')}/{dados.get('uf', '')}"
            }
            for nome, valor in endereco.items():
                campos[nome].delete(0, tk.END)
                campos[nome].insert(0, valor)

            messagebox.showinfo('CEP encontrado', 'Endereço preenchido com sucesso!')
    except queue.Empty:
        pass
    janela.after(100, verificar_respostas_cep)


botao_cep = ttk.Button(frame_formulario, text='Buscar CEP', command=buscar_cep)
botao_cep.grid(row=5, column=3, padx=5, pady=10, sticky='e')

# Tabela de registros
frame_tabela = ttk.LabelFrame(janela, text='Agendamentos Cadastrados', padding=10)
frame_tabela.pack(fill='both', expand=True, padx=20, pady=10)
colunas = ('ID', 'Pet', 'Tutor', 'Telefone', 'Serviço', 'Data/Horário')
tabela = ttk.Treeview(frame_tabela, columns=colunas, show='headings', height=10)
for coluna in colunas:
    tabela.heading(coluna, text=coluna)
    tabela.column(coluna, width=130, anchor='center')
for coluna, largura in {
    'ID': 50, 'Pet': 120, 'Tutor': 160, 'Telefone': 120,
    'Serviço': 130, 'Data/Horário': 150,
}.items():
    tabela.column(coluna, width=largura)
barra_rolagem = ttk.Scrollbar(frame_tabela, orient='vertical', command=tabela.yview)
tabela.configure(yscrollcommand=barra_rolagem.set)
barra_rolagem.pack(side='right', fill='y')
tabela.pack(fill='both', expand=True)


def carregar_agendamentos():
    for item in tabela.get_children():
        tabela.delete(item)
    for agendamento in listar_agendamentos():
        tabela.insert('', 'end', values=(
            agendamento[0], agendamento[1], agendamento[2],
            agendamento[3], agendamento[9], agendamento[10]
        ))


frame_botoes = ttk.Frame(janela)
frame_botoes.pack(pady=10)


def obter_dados_formulario():
    return {
        'nome_pet': campos['Nome do Pet'].get().strip(),
        'tutor': campos['Tutor'].get().strip(),
        'telefone': campos['Telefone'].get().strip(),
        'cep': campos['CEP'].get().strip(),
        'logradouro': campos['Logradouro'].get().strip(),
        'bairro': campos['Bairro'].get().strip(),
        'cidade_uf': campos['Cidade/UF'].get().strip(),
        'numero': campos['Número'].get().strip(),
        'servico': combo_servico.get().strip(),
        'data_horario': campos['Data/Horário'].get().strip(),
    }


def validar_formulario(dados):
    for campo, valor in dados.items():
        if not valor:
            messagebox.showwarning('Campo obrigatório', f'Preencha o campo: {campo}')
            return False
    return True


def limpar():
    global id_selecionado
    id_selecionado = None
    # Cancela a seleção antes de limpar para evitar novo preenchimento.
    for item in tabela.selection():
        tabela.selection_remove(item)
    for entrada in campos.values():
        entrada.delete(0, tk.END)
    combo_servico.set('Consulta')


def cadastrar():
    dados = obter_dados_formulario()
    if not validar_formulario(dados):
        return

    resultado = cadastrar_agendamento(
        dados['nome_pet'], dados['tutor'], dados['telefone'], dados['cep'],
        dados['logradouro'], dados['bairro'], dados['cidade_uf'],