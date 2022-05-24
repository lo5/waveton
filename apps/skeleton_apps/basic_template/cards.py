import sys
import traceback

from h2o_wave import ui, Q, expando_to_dict

issue_link = 'https://github.com/vopani/waveton/issues/new?assignees=vopani&labels=bug&template=error-report.md&title=%5BERROR%5D'


def create_error_report(q: Q) -> ui.FormCard:
    """
    Card for handling crash.
    """

    def code_block(content): return '\n'.join(['```', *content, '```'])

    type_, value_, traceback_ = sys.exc_info()
    stack_trace = traceback.format_exception(type_, value_, traceback_)

    dump = [
        '### Stack Trace',
        code_block(stack_trace),
    ]

    states = [
        ('q.app', q.app),
        ('q.user', q.user),
        ('q.client', q.client),
        ('q.events', q.events),
        ('q.args', q.args),
    ]
    for name, source in states:
        dump.append(f'### {name}')
        dump.append(code_block([f'{k}: {v}' for k, v in expando_to_dict(source).items()]))

    return ui.form_card(
        box='error',
        items=[
            ui.stats(
                items=[
                    ui.stat(
                        label='',
                        value='Oops!',
                        caption='Something went wrong',
                        icon='Error'
                    )
                ],
            ),
            ui.separator(),
            ui.text_l(content='Apologies for the inconvenience!'),
            ui.buttons(items=[ui.button(name='restart', label='Restart', primary=True)]),
            ui.expander(name='report', label='Error Details', items=[
                ui.text(f'To report this issue, <a href="{issue_link}" target="_blank">please open an issue</a> with the details below:'),
                ui.text_l(content='Report Issue in App: **Basic Template**'),
                ui.text(content='\n'.join(dump)),
            ]),
        ]
    )
