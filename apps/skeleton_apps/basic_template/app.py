import logging

from h2o_wave import Q, main, app, ui, handle_on, on

import cards

logging.basicConfig(format='%(levelname)s:\t[%(asctime)s]\t%(message)s', level=logging.INFO)


@app('/')
async def serve(q: Q):
    """
    App function.
    """

    try:
        # initialize app
        if not q.app.initialized:
            await initialize_app(q)

        # initialize client
        if not q.client.initialized:
            await initialize_client(q)

        # handle ons
        elif await handle_on(q):
            pass

        # dummy update for edge cases
        else:
            await update_dummy(q)

    except Exception as error:
        await show_error(q, error=str(error))


async def initialize_app(q: Q):
    """
    Initializing app.
    """

    logging.info('Initializing app')

    q.app.initialized = True


async def initialize_client(q: Q):
    """
    Initializing client.
    """

    logging.info('Initializing client')

    q.page['meta'] = ui.meta_card(
        box='',
        title='WaveTon',
        layouts=[
            ui.layout(
                breakpoint='xs',
                zones=[
                    ui.zone(name='header'),
                    ui.zone(name='home'),
                    ui.zone(name='error'),
                    ui.zone(name='footer')
                ]
            )
        ],
        theme='h2o-dark'
    )
    q.page['header'] = ui.header_card(
        box='header',
        title='Basic Template',
        subtitle='Building blocks to kickstart an app',
        icon='BuildQueue',
        icon_color='black'
    )
    q.page['home'] = ui.form_card(
        box='home',
        items=[
            ui.text('This is a great starting point to build an app.')
        ]
    )
    q.page['footer'] = ui.footer_card(
        box='footer',
        caption='Learn more about <a href="https://github.com/vopani/waveton" target="_blank"> WaveTon: 💯 Wave Applications</a>'
    )

    q.page['dummy'] = ui.form_card(
        box='dummy',
        items=[]
    )

    q.client.initialized = True

    await q.page.save()


def drop_cards(q: Q, card_names: list):
    """
    Drop cards from Wave page.
    """

    logging.info('Clearing cards')

    for card_name in card_names:
        del q.page[card_name]


async def show_error(q: Q, error: str):
    """
    Handle any app error.
    """

    logging.error(error)

    drop_cards(q, ['home'])

    q.page['error'] = cards.create_error_report(q)

    await q.page.save()


@on('restart')
async def restart(q: Q):
    """
    Restart app.
    """

    logging.info('Restarting app')

    await initialize_client(q)


async def update_dummy(q: Q):
    """
    Dummy update for edge cases.
    """

    logging.info('Adding dummy page')

    q.page['dummy'].items = []

    await q.page.save()
