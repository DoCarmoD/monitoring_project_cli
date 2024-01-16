from datetime import datetime
from time import sleep
from dashing import HSplit, VSplit, VGauge, HGauge, Text
from psutil import virtual_memory, swap_memory,cpu_percent,process_iter



ui = HSplit(  # ui
    VSplit(
        Text(
            ' ',
            border_color=9,
            title='Processos'
        ),
        HSplit(  # ui.items[0]
            VGauge(title='RAM'),  # ui.items[0].items[0]
            VGauge(title='SWAP'),  # ui.items[0].items[1]
            title='Memória',
            border_color=3
        ),
    ),
    VSplit(  # ui.items[1]
        HGauge(title='CPU %'),
        HGauge(title='core 0'),
        HGauge(title='core 1'),
        HGauge(title='core 2'),
        HGauge(title='core 3'),
        HGauge(title='core 4'),
        HGauge(title='core 5'),
        HGauge(title='core 6'),
        HGauge(title='core 7'),
        title='CPU',#Aqui coloque o modelo do seu processador, por padrão vem setado como CPU 
        border_color=5,
    ),title="DoCarmo Dev",
        border_color=2,
)

while True:
    # # Processos
    proc_tui = ui.items[0].items[0]
    p_list = []
    for proc in process_iter():
        proc_info = proc.as_dict(['name', 'cpu_percent'])
        if proc_info['cpu_percent'] > 0:
            p_list.append(proc_info)

    ordenados = sorted(
        p_list,
        key=lambda p: p['cpu_percent'],
        reverse=True
    )[:10]
    proc_tui.text = f"{'Nome':<30}CPU"

    for proc in ordenados:
        proc_tui.text += f"\n{proc['name']:<30} {proc['cpu_percent']}"

    
    
    # # Memória
    mem_tui = ui.items[0].items[1]
    # Ram
    ram_tui = mem_tui.items[0]
    ram_tui.value = virtual_memory().percent
    ram_tui.title = f'RAM {ram_tui.value} %'

    # SWAP
    swap_tui = mem_tui.items[1]
    swap_tui.value = swap_memory().percent
    swap_tui.title = f'SWAP {swap_tui.value} %'

    # # CPU
    cpu_tui = ui.items[1]
    # CPU %
    cpu_percent_tui = cpu_tui.items[0]
    ps_cpu_percent = cpu_percent()
    cpu_percent_tui.value = ps_cpu_percent
    cpu_percent_tui.title = f'CPU {ps_cpu_percent}%'

    # Porcentagem dos cores
    cores_tui = cpu_tui.items[1:9]
    ps_cpu_percent = cpu_percent(percpu=True)
    for i, (core, value) in enumerate(zip(cores_tui, ps_cpu_percent)):
        core.value = value
        core.title = f'cpu_{i} {value}%'

    try:
        ui.display()
        sleep(1)
    except KeyboardInterrupt:
        break
