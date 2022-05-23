import sys
import traceback

import pandas as pd

from h2o_wave import ui

import layouts
from constants import EdgeDetectionKernels


def meta() -> ui.MetaCard:
    """
    Card for meta information.
    """

    card = ui.meta_card(
        box='',
        title='WaveTon',
        layouts=[
            layouts.default()
        ],
        theme='h2o-dark'
    )

    return card


def error(q_app: dict, q_user: dict, q_client: dict, q_events: dict, q_args: dict) -> ui.FormCard:
    """
    Card for handling crash.
    """

    q_app_str = '### q.app\n```' + '\n'.join([f'{k}: {v}' for k, v in q_app.items()]) + '\n```'
    q_user_str = '### q.user\n```' + '\n'.join([f'{k}: {v}' for k, v in q_user.items()]) + '\n```'
    q_client_str = '### q.client\n```' + '\n'.join([f'{k}: {v}' for k, v in q_client.items()]) + '\n```'
    q_events_str = '### q.events\n```' + '\n'.join([f'{k}: {v}' for k, v in q_events.items()]) + '\n```'
    q_args_str = '### q.args\n```' + '\n'.join([f'{k}: {v}' for k, v in q_args.items()]) + '\n```'

    type_, value_, traceback_ = sys.exc_info()
    stack_trace = traceback.format_exception(type_, value_, traceback_)
    stack_trace_str = '### stacktrace\n' + '\n'.join(stack_trace)

    card = ui.form_card(
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
                justify='center'
            ),
            ui.separator(),
            ui.text_l(content='<center>Apologies for the inconvenience!</center>'),
            ui.buttons(
                items=[
                    ui.button(name='restart', label='Restart', primary=True),
                    ui.button(name='report', label='Report', primary=True)
                ],
                justify='center'
            ),
            ui.separator(visible=False),
            ui.text(
                content='''<center>
                    To report this issue, please open an issue on 
                    <a href="https://github.com/vopani/waveton/issues/new" target="_blank">https://github.com/vopani/waveton/issues/new</a>
                    with the details below:</center>''',
                visible=False
            ),
            ui.text_l(content='Report Issue in App: **NER Annotation**', visible=False),
            ui.text(content=q_app_str, visible=False),
            ui.text(content=q_user_str, visible=False),
            ui.text(content=q_client_str, visible=False),
            ui.text(content=q_events_str, visible=False),
            ui.text(content=q_args_str, visible=False),
            ui.text(content=stack_trace_str, visible=False)
        ]
    )

    return card


def header() -> ui.HeaderCard:
    """
    Card for header.
    """

    card = ui.header_card(
        box='header',
        title='Edge Detector',
        subtitle='Tool to visualize edge detection algorithms',
        icon='ImageSearch',
        icon_color='black',
        items=[
            ui.toggle(name='theme_dark', label='Dark Mode', value=True, trigger=True)
        ]
    )

    return card


def footer() -> ui.FooterCard:
    """
    Card for footer.
    """

    card = ui.footer_card(
        box='footer',
        caption='Learn more about <a href="https://github.com/vopani/waveton" target="_blank">WaveTon: 💯 Wave Applications</a>'
    )

    return card


def command_panel(edge_detection_kernel, gaussian_blur, gaussian_kernel_size) -> ui.FormCard:
    """
    Card for control panel.
    """

    kernel_choices = [
        ui.choice(
            name=EdgeDetectionKernels.LAPLACE.value,
            label=EdgeDetectionKernels.LAPLACE.value
        ),
        ui.choice(
            name=EdgeDetectionKernels.SOBEL.value,
            label=EdgeDetectionKernels.SOBEL.value
        )
    ]

    return ui.form_card(
        box='commands',
        items=[
            ui.text_xl("Command Panel"),
            ui.file_upload(
                name="image_uploader",
                label="Upload",
                multiple=False,
                file_extensions=['jpeg', 'png'],
            ),
            ui.separator(),
            ui.text_xl("Kernel Configurations"),
            ui.choice_group(
                name="edge_detection_kernel",
                label="Select Kernel",
                choices=kernel_choices,
                value=edge_detection_kernel
            ),
            ui.separator(),
            ui.text_xl("Blur Configurations"),
            ui.checkbox(
                name="gaussian_blur",
                label="Apply Gaussian Blur for Smoothing",
                value=gaussian_blur,
            ),
            ui.text_xl("\n"),
            ui.slider(
                name="gaussian_kernel_size",
                label="Blur Kernel Size",
                min=3,
                max=21,
                step=2,
                value=gaussian_kernel_size
            ),
            ui.text_xl("\n"),
            ui.buttons(
                items=[
                    ui.button(
                        name="run_edge_detection",
                        label="Detect",
                        primary=True,
                        icon="Search"
                    )
                ]
            )

        ],
    )


def original_image_viewer(image_path) -> ui.ImageCard:
    """
    Card to display original image.
    """
    return ui.image_card(
        box='main_top_left',
        title="Original Image",
        path=image_path
    )


def processed_image_viewer(image_path) -> ui.ImageCard:
    """
    Card to display processed image.
    """
    return ui.image_card(
        box='main_top_right',
        title="Processed Image",
        path=image_path
    )


def image_table(image_df: pd.DataFrame) -> ui.FormCard:
    """
    Card to display uploaded image table.
    """
    columns = [
        ui.table_column(
            name="image_name",
            label="Image",
            sortable=True,
            searchable=True,
            link=True,
            max_width="750px"
        ),
        ui.table_column(
            name="uploaded_time",
            label="Uploaded At",
            sortable=True,
        )
    ]

    rows = [
        ui.table_row(
            name=row.Image,
            cells=[row.Image, row.Timestamp]
        ) for row in image_df.itertuples()
    ]

    table = ui.table(
        name="image_table",
        columns=columns,
        rows=rows,
        height='calc(((100vh - 150px)/3) - 75px)'
    )
    return ui.form_card(
        box='main_bottom',
        items=[
            table
        ]
    )
