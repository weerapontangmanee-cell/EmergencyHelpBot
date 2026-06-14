from linebot.models import (
    FlexSendMessage,
    BubbleContainer,
    BoxComponent,
    TextComponent,
    SeparatorComponent,
)


COLOR_PRIMARY = "#E53935"       # แดง - หัวข้อ
COLOR_STEP_NUM = "#1E88E5"      # น้ำเงิน - เลขขั้นตอน
COLOR_DONT_BG = "#FFEBEE"       # แดงอ่อน - พื้นกล่องห้ามทำ
COLOR_DONT_TEXT = "#C62828"     # แดงเข้ม - ข้อความห้ามทำ
COLOR_WARNING_BG = "#FFF3E0"    # ส้มอ่อน - พื้นกล่องคำเตือน
COLOR_WARNING_TEXT = "#E65100"  # ส้มเข้ม - ข้อความคำเตือน


def _step_row(number, text):
    """แถวขั้นตอน: วงกลมเลขสีน้ำเงิน + ข้อความ"""
    return BoxComponent(
        layout="horizontal",
        spacing="md",
        margin="md",
        contents=[
            BoxComponent(
                layout="vertical",
                width="24px",
                height="24px",
                corner_radius="12px",
                background_color=COLOR_STEP_NUM,
                justify_content="center",
                align_items="center",
                contents=[
                    TextComponent(
                        text=str(number),
                        size="xs",
                        color="#FFFFFF",
                        weight="bold",
                        align="center",
                    )
                ],
            ),
            TextComponent(
                text=text,
                size="sm",
                color="#333333",
                wrap=True,
                flex=1,
            ),
        ],
    )


def _dont_row(text):
    """แถวรายการห้ามทำ"""
    return BoxComponent(
        layout="baseline",
        spacing="sm",
        margin="sm",
        contents=[
            TextComponent(
                text="✕",
                size="sm",
                color=COLOR_DONT_TEXT,
                flex=0,
                weight="bold",
            ),
            TextComponent(
                text=text,
                size="sm",
                color=COLOR_DONT_TEXT,
                wrap=True,
                flex=1,
            ),
        ],
    )


def build_flex(case_key, case_data):
    """
    สร้าง FlexSendMessage จากข้อมูล 1 เคส
    case_data ต้องมี: emoji, title, steps (list), donts (list), warning (str)
    """

    body_contents = []

    # หัวข้อ
    body_contents.append(
        TextComponent(
            text=f"{case_data['emoji']} {case_data['title']}",
            weight="bold",
            size="lg",
            color=COLOR_PRIMARY,
            wrap=True,
        )
    )

    body_contents.append(SeparatorComponent(margin="md"))

    # หัวข้อย่อย: วิธีปฐมพยาบาล
    body_contents.append(
        TextComponent(
            text="วิธีปฐมพยาบาล",
            weight="bold",
            size="md",
            color="#333333",
            margin="md",
        )
    )

    # ขั้นตอน
    for i, step in enumerate(case_data["steps"], start=1):
        body_contents.append(_step_row(i, step))

    # กล่องห้ามทำ
    if case_data.get("donts"):
        dont_box_contents = [
            TextComponent(
                text="❌ สิ่งที่ห้ามทำ",
                weight="bold",
                size="md",
                color=COLOR_DONT_TEXT,
            )
        ]
        for dont in case_data["donts"]:
            dont_box_contents.append(_dont_row(dont))

        body_contents.append(
            BoxComponent(
                layout="vertical",
                margin="lg",
                padding_all="12px",
                corner_radius="8px",
                background_color=COLOR_DONT_BG,
                contents=dont_box_contents,
            )
        )

    # กล่องคำเตือน / เมื่อไหร่ต้องโทร 1669
    if case_data.get("warning"):
        body_contents.append(
            BoxComponent(
                layout="vertical",
                margin="md",
                padding_all="12px",
                corner_radius="8px",
                background_color=COLOR_WARNING_BG,
                contents=[
                    TextComponent(
                        text="⚠️ เมื่อไหร่ต้องโทร 1669",
                        weight="bold",
                        size="md",
                        color=COLOR_WARNING_TEXT,
                    ),
                    TextComponent(
                        text=case_data["warning"],
                        size="sm",
                        color=COLOR_WARNING_TEXT,
                        wrap=True,
                        margin="sm",
                    ),
                ],
            )
        )

    bubble = BubbleContainer(
        body=BoxComponent(
            layout="vertical",
            padding_all="16px",
            contents=body_contents,
        )
    )

    return FlexSendMessage(
        alt_text=f"{case_data['emoji']} {case_data['title']}",
        contents=bubble,
    )