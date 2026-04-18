from uuid import uuid4

from deps_document_layout.model import EntityId, Point, TenantId
from deps_document_layout.model.document_layout import *

page1_id = "a70200f10b65443b97a393f40c1e54c2"
page2_id = "f361997ff51f4827b7dda192973fb93a"
file_path1 = "ecf5d37bf4944ff7b290670b523652dc"
file_path2 = "2fb9e0ebd9674250824e1cbb1c2c80e8"
image_title1 = "06b52904738a475791f7eecd1db4f685"
image_file_path1 = "8833fdb9d36544e0b0d153008b74aea8"
image_file_path2 = "fb00d04bf4a643938a91ad2bbaad9111"
document_layout_id = "e44f842e3f0c4b62afb076156446f5ec"
tenant_id = "1d92ba891bb74bac824b4f62e9b4e2e0"
image_description = "b7fd0304e62a44cba6478e4b92fc1823"

page_1_images_ids = [uuid4().hex for _ in range(5)]
page_1_kvps_ids = [uuid4().hex for _ in range(5)]
page_1_table_ids = [uuid4().hex for _ in range(5)]
page_1_paragraph_ids = [uuid4().hex for _ in range(5)]

page_2_images_ids = [uuid4().hex for _ in range(5)]
page_2_kvps_ids = [uuid4().hex for _ in range(5)]
page_2_table_ids = [uuid4().hex for _ in range(5)]
page_2_paragraph_ids = [uuid4().hex for _ in range(5)]

group_1_id = uuid4().hex
group_1_members = [page_1_images_ids[0]]
group_2_id = uuid4().hex
group_2_members = [page_2_images_ids[0]]
parsing_features = {ParsingType.AZURE_FORM_RECOGNIZER: {ParsingFeature.TABLES, ParsingFeature.IMAGES}}

page_1_with_images_kv_pairs_tables_paragraphs = Page(
    id_=EntityId(page1_id),
    page_number=1,
    parsing_type=ParsingType.AWS_TEXTRACT,
    dimension=Dimension(width=1000, height=1000, unit="px"),
    languages=(Language(language_code="eng", confidence=1.0),),
    file_path=file_path1,
    transformations=Transformations(
        thresholding=Thresholding(low_value=2, high_value=2, flag=2),
        blurring=Blurring(kernel=(2, 2), sigma=1.0),
    ),
    images=(
        Image(
            id_=EntityId(page_1_images_ids[0]),
            order=0,
            title=image_title1,
            file_path=image_file_path1,
            polygon=(
                Point(x=0.1, y=0.1),
                Point(x=0.3, y=0.1),
                Point(x=0.3, y=0.3),
                Point(x=0.1, y=0.3),
            ),
            description=image_description,
        ),
    ),
    key_value_pairs=(
        KeyValuePair(
            id_=EntityId(page_1_kvps_ids[0]),
            key=KeyValuePairElement(
                content="Balance",
                polygon=(
                    Point(x=0.7792459726333618, y=0.7385748624801636),
                    Point(x=0.8397561311721802, y=0.7386471629142761),
                    Point(x=0.8397284746170044, y=0.750789225101471),
                    Point(x=0.7792187333106995, y=0.7507163286209106),
                ),
            ),
            value=KeyValuePairElement(
                content="$ 125.09",
                polygon=(
                    Point(x=0.8828075528144836, y=0.7378674745559692),
                    Point(x=0.9610974192619324, y=0.7379609942436218),
                    Point(x=0.9610683917999268, y=0.7503637075424194),
                    Point(x=0.882779061794281, y=0.7502694725990295),
                ),
            ),
            confidence=0.999250,
            order=0,
        ),
        KeyValuePair(
            id_=EntityId(page_1_kvps_ids[1]),
            key=KeyValuePairElement(
                content="Signature:",
                polygon=(
                    Point(x=0.09872318059206009, y=0.8909910917282104),
                    Point(x=0.16686254739761353, y=0.8910802602767944),
                    Point(x=0.16683751344680786, y=0.9041547775268555),
                    Point(x=0.09869863092899323, y=0.904064953327179),
                ),
            ),
            value=None,
            confidence=0.916803,
            order=1,
        ),
    ),
    tables=(
        Table(
            id_=EntityId(page_1_table_ids[0]),
            order=1,
            column_count=4,
            row_count=2,
            polygon=(
                Point(x=0.09854213893413544, y=0.3893252909183502),
                Point(x=0.9805532693862915, y=0.39015230536460876),
                Point(x=0.9804075956344604, y=0.4520988464355469),
                Point(x=0.09842590242624283, y=0.4512314796447754),
            ),
            confidence=0.975097,
            cells=(
                Cell(
                    content="EVENT",
                    column_index=1,
                    column_span=1,
                    row_index=1,
                    row_span=1,
                    polygon=(
                        Point(x=0.09854213893413544, y=0.3893252909183502),
                        Point(x=0.9805532693862915, y=0.39015230536460876),
                        Point(x=0.9804075956344604, y=0.4520988464355469),
                        Point(x=0.09842590242624283, y=0.4512314796447754),
                    ),
                    kind="COLUMN_HEADER",
                ),
                Cell(
                    content="DATE",
                    column_index=2,
                    column_span=1,
                    row_index=1,
                    row_span=1,
                    polygon=(
                        Point(x=0.3996262550354004, y=0.38960760831832886),
                        Point(x=0.6569868326187134, y=0.389848917722702),
                        Point(x=0.6569215059280396, y=0.41985729336738586),
                        Point(x=0.39956507086753845, y=0.41961026191711426),
                    ),
                    kind="COLUMN_HEADER",
                ),
                Cell(
                    content="LOCATION",
                    column_index=3,
                    column_span=1,
                    row_index=1,
                    row_span=1,
                    polygon=(
                        Point(x=0.6569868326187134, y=0.389848917722702),
                        Point(x=0.8123155832290649, y=0.3899945616722107),
                        Point(x=0.8122477531433105, y=0.4200063645839691),
                        Point(x=0.6569215059280396, y=0.41985729336738586),
                    ),
                    kind="COLUMN_HEADER",
                ),
                Cell(
                    content="DUE DATE",
                    column_index=4,
                    column_span=1,
                    row_index=1,
                    row_span=1,
                    polygon=(
                        Point(x=0.8123155832290649, y=0.3899945616722107),
                        Point(x=0.9805532693862915, y=0.39015230536460876),
                        Point(x=0.9804826378822327, y=0.42016786336898804),
                        Point(x=0.8122477531433105, y=0.4200063645839691),
                    ),
                    kind="COLUMN_HEADER",
                ),
                Cell(
                    content="",
                    column_index=1,
                    column_span=1,
                    row_index=2,
                    row_span=1,
                    polygon=(
                        Point(x=0.09848581999540329, y=0.41932129859924316),
                        Point(x=0.39956507086753845, y=0.41961026191711426),
                        Point(x=0.3994999825954437, y=0.45152756571769714),
                        Point(x=0.09842590242624283, y=0.4512314796447754),
                    ),
                ),
                Cell(
                    content="April 14, 2011",
                    column_index=2,
                    column_span=1,
                    row_index=2,
                    row_span=1,
                    polygon=(
                        Point(x=0.39956507086753845, y=0.41961026191711426),
                        Point(x=0.6569215059280396, y=0.41985729336738586),
                        Point(x=0.6568519473075867, y=0.45178064703941345),
                        Point(x=0.3994999825954437, y=0.45152756571769714),
                    ),
                ),
                Cell(
                    content="Valdosta, Georgia",
                    column_index=3,
                    column_span=1,
                    row_index=2,
                    row_span=1,
                    polygon=(
                        Point(x=0.6569215059280396, y=0.41985729336738586),
                        Point(x=0.8122477531433105, y=0.4200063645839691),
                        Point(x=0.8121755719184875, y=0.4519333839416504),
                        Point(x=0.6568519473075867, y=0.45178064703941345),
                    ),
                ),
                Cell(
                    content="Due upon receipt of documents",
                    column_index=4,
                    column_span=1,
                    row_index=2,
                    row_span=1,
                    polygon=(
                        Point(x=0.8122477531433105, y=0.4200063645839691),
                        Point(x=0.9804826378822327, y=0.42016786336898804),
                        Point(x=0.9804075956344604, y=0.4520988464355469),
                        Point(x=0.8121755719184875, y=0.4519333839416504),
                    ),
                ),
            ),
        ),
    ),
    paragraphs=(
        Paragraph(
            id_=EntityId(page_1_paragraph_ids[0]),
            order=2,
            content="VALDOSTA LOWNDES COUNTY\nIndustrial Authority",
            polygon=(
                Point(x=0.12720482051372528, y=0.06185947731137276),
                Point(x=0.45422646403312683, y=0.06185947731137276),
                Point(x=0.45422646403312683, y=0.104300357401371),
                Point(x=0.12720482051372528, y=0.104300357401371),
            ),
            confidence=0.953004,
            role="HEADER",
            lines=(
                Line(
                    order=0,
                    content="VALDOSTA LOWNDES COUNTY",
                    polygon=(
                        Point(x=0.16565455496311188, y=0.06168489530682564),
                        Point(x=0.4166678488254547, y=0.06185947731137276),
                        Point(x=0.4166451096534729, y=0.07296974211931229),
                        Point(x=0.16563330590724945, y=0.07279309630393982),
                    ),
                    confidence=0.953004,
                    words=(
                        Word(
                            order=0,
                            content="VALDOSTA",
                            confidence=0.972114,
                            polygon=(
                                Point(x=0.16565382480621338, y=0.06206876039505005),
                                Point(x=0.2470325380563736, y=0.06212538108229637),
                                Point(x=0.24701187014579773, y=0.07268821448087692),
                                Point(x=0.16563360393047333, y=0.07263095676898956),
                            ),
                            style=Style(
                                background_color="white",
                                color="black",
                                bold=True,
                                italic=True,
                                handwritten=False,
                                font_type="Calibri",
                                font_size="14pt",
                                underlined=False,
                                strikeout=False,
                                subscript=False,
                                superscript=False,
                                smallcaps=True,
                            ),
                        ),
                        Word(
                            order=1,
                            content="LOWNDES",
                            confidence=0.897392,
                            polygon=(
                                Point(x=0.26604604721069336, y=0.06175471842288971),
                                Point(x=0.3445536196231842, y=0.061809320002794266),
                                Point(x=0.34453144669532776, y=0.07284170389175415),
                                Point(x=0.2660243511199951, y=0.07278646528720856),
                            ),
                            style=Style(
                                background_color="white",
                                color="black",
                                bold=True,
                                italic=True,
                                handwritten=False,
                                font_type="Calibri",
                                font_size="14pt",
                                underlined=False,
                                strikeout=False,
                                subscript=False,
                                superscript=False,
                                smallcaps=True,
                            ),
                        ),
                        Word(
                            order=2,
                            content="COUNTY",
                            confidence=0.989505,
                            polygon=(
                                Point(x=0.3487030565738678, y=0.06196937710046768),
                                Point(x=0.41666755080223083, y=0.06201665475964546),
                                Point(x=0.4166451096534729, y=0.07296974211931229),
                                Point(x=0.3486810326576233, y=0.07292190939188004),
                            ),
                            style=Style(
                                background_color="white",
                                color="black",
                                bold=True,
                                italic=True,
                                handwritten=False,
                                font_type="Calibri",
                                font_size="14pt",
                                underlined=False,
                                strikeout=False,
                                subscript=False,
                                superscript=False,
                                smallcaps=True,
                            ),
                        ),
                    ),
                ),
                Line(
                    order=1,
                    content="Industrial Authority",
                    polygon=(
                        Point(x=0.12726040184497833, y=0.0746949315071106),
                        Point(x=0.45422646403312683, y=0.0749254897236824),
                        Point(x=0.4541656970977783, y=0.104300357401371),
                        Point(x=0.12720482051372528, y=0.10406270623207092),
                    ),
                    confidence=0.999470,
                    words=(
                        Word(
                            order=0,
                            content="Industrial",
                            confidence=0.999091,
                            polygon=(
                                Point(x=0.12726040184497833, y=0.0746949315071106),
                                Point(x=0.2879866063594818, y=0.074808269739151),
                                Point(x=0.2879401743412018, y=0.09826946258544922),
                                Point(x=0.12721601128578186, y=0.09815333783626556),
                            ),
                            style=Style(
                                background_color="white",
                                color="black",
                                bold=True,
                                italic=False,
                                handwritten=False,
                                font_type="Abadi",
                                font_size="14pt",
                                underlined=False,
                                strikeout=False,
                                subscript=False,
                                superscript=False,
                                smallcaps=False,
                            ),
                        ),
                        Word(
                            order=1,
                            content="Authority",
                            confidence=0.999850,
                            polygon=(
                                Point(x=0.29450589418411255, y=0.07486402243375778),
                                Point(x=0.4542263448238373, y=0.07497665286064148),
                                Point(x=0.4541656970977783, y=0.104300357401371),
                                Point(x=0.29444774985313416, y=0.10418426245450974),
                            ),
                            style=Style(
                                background_color="white",
                                color="black",
                                bold=True,
                                italic=False,
                                handwritten=False,
                                font_type="Abadi",
                                underlined=False,
                                strikeout=False,
                                subscript=False,
                                superscript=False,
                                smallcaps=False,
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),
    groups=(
        Group(id_=EntityId(group_1_id), name="Page1 Group", members=frozenset([EntityId(x) for x in group_1_members])),
    ),
)

page_2_with_images_kv_pairs_tables_paragraphs = Page(
    id_=EntityId(page2_id),
    page_number=2,
    parsing_type=ParsingType.AWS_TEXTRACT,
    dimension=Dimension(width=1005, height=1005, unit="px"),
    languages=(Language(language_code="eng", confidence=1.0),),
    file_path=file_path2,
    transformations=Transformations(thresholding=Thresholding(low_value=3, high_value=3, flag=1)),
    groups=(
        Group(id_=EntityId(group_2_id), name="Page2 Group", members=frozenset([EntityId(x) for x in group_2_members])),
    ),
    images=(
        Image(
            id_=EntityId(page_2_images_ids[0]),
            order=0,
            file_path=image_file_path2,
            polygon=(
                Point(x=0.2, y=0.2),
                Point(x=0.4, y=0.2),
                Point(x=0.4, y=0.4),
                Point(x=0.2, y=0.4),
            ),
        ),
    ),
    key_value_pairs=(
        KeyValuePair(
            id_=EntityId(page_2_kvps_ids[0]),
            key=KeyValuePairElement(
                content="AIRWAY BILL NO.",
                polygon=(
                    Point(x=0.11943134665489197, y=0.1489686369895935),
                    Point(x=0.21852388978004456, y=0.1489812731742859),
                    Point(x=0.21852533519268036, y=0.15784229338169098),
                    Point(x=0.11943251639604568, y=0.1578296720981598),
                ),
            ),
            value=KeyValuePairElement(
                content="000231",
                polygon=(
                    Point(x=0.1181400939822197, y=0.16277551651000977),
                    Point(x=0.16564106941223145, y=0.16278156638145447),
                    Point(x=0.1656423807144165, y=0.17165611684322357),
                    Point(x=0.11814125627279282, y=0.17165008187294006),
                ),
            ),
            confidence=0.933754,
            order=0,
        ),
        KeyValuePair(
            id_=EntityId(page_2_kvps_ids[1]),
            key=KeyValuePairElement(
                content="EMAIL",
                polygon=(
                    Point(x=0.5561466217041016, y=0.33884578943252563),
                    Point(x=0.592820405960083, y=0.3388502895832062),
                    Point(x=0.5928229689598083, y=0.34754979610443115),
                    Point(x=0.5561490058898926, y=0.347545325756073),
                ),
            ),
            value=KeyValuePairElement(
                content="",
                polygon=(
                    Point(x=0.7116237282752991, y=0.3391474485397339),
                    Point(x=0.8342684507369995, y=0.3391624093055725),
                    Point(x=0.8342725038528442, y=0.3502322733402252),
                    Point(x=0.7116273641586304, y=0.350217342376709),
                ),
            ),
            confidence=0.930332,
            order=1,
        ),
    ),
    tables=(
        Table(
            id_=EntityId(page_2_table_ids[0]),
            order=1,
            column_count=4,
            row_count=2,
            polygon=(
                Point(x=0.11592782288789749, y=0.14602451026439667),
                Point(x=0.8904334306716919, y=0.14612334966659546),
                Point(x=0.8904438018798828, y=0.1729148030281067),
                Point(x=0.11593133211135864, y=0.17281654477119446),
            ),
            confidence=0.815917,
            cells=(
                Cell(
                    content="AIRWAY BILL NO.",
                    column_index=1,
                    column_span=1,
                    row_index=1,
                    row_span=1,
                    polygon=(
                        Point(x=0.11592782288789749, y=0.14602451026439667),
                        Point(x=0.28105443716049194, y=0.14604558050632477),
                        Point(x=0.2810569405555725, y=0.15960046648979187),
                        Point(x=0.11592959612607956, y=0.15957945585250854),
                    ),
                    kind="COLUMN_HEADER",
                ),
                Cell(
                    content="INVOICE NO.",
                    column_index=2,
                    column_span=1,
                    row_index=1,
                    row_span=1,
                    polygon=(
                        Point(x=0.28105443716049194, y=0.14604558050632477),
                        Point(x=0.4835886061191559, y=0.1460714340209961),
                        Point(x=0.48359203338623047, y=0.15962623059749603),
                        Point(x=0.2810569405555725, y=0.15960046648979187),
                    ),
                    kind="COLUMN_HEADER",
                ),
                Cell(
                    content="INVOICE DATE",
                    column_index=3,
                    column_span=1,
                    row_index=1,
                    row_span=1,
                    polygon=(
                        Point(x=0.4835886061191559, y=0.1460714340209961),
                        Point(x=0.7029619812965393, y=0.14609943330287933),
                        Point(x=0.7029663920402527, y=0.1596541404724121),
                        Point(x=0.48359203338623047, y=0.15962623059749603),
                    ),
                    kind="COLUMN_HEADER",
                ),
                Cell(
                    content="DATE OF EXPORT",
                    column_index=4,
                    column_span=1,
                    row_index=1,
                    row_span=1,
                    polygon=(
                        Point(x=0.7029619812965393, y=0.14609943330287933),
                        Point(x=0.8904334306716919, y=0.14612334966659546),
                        Point(x=0.8904386758804321, y=0.15967799723148346),
                        Point(x=0.7029663920402527, y=0.1596541404724121),
                    ),
                    kind="COLUMN_HEADER",
                ),
                Cell(
                    content="000231",
                    column_index=1,
                    column_span=1,
                    row_index=2,
                    row_span=1,
                    polygon=(
                        Point(x=0.11592959612607956, y=0.15957945585250854),
                        Point(x=0.2810569405555725, y=0.15960046648979187),
                        Point(x=0.2810593843460083, y=0.172837495803833),
                        Point(x=0.11593133211135864, y=0.17281654477119446),
                    ),
                ),
                Cell(
                    content="000562",
                    column_index=2,
                    column_span=1,
                    row_index=2,
                    row_span=1,
                    polygon=(
                        Point(x=0.2810569405555725, y=0.15960046648979187),
                        Point(x=0.48359203338623047, y=0.15962623059749603),
                        Point(x=0.4835953712463379, y=0.1728632003068924),
                        Point(x=0.2810593843460083, y=0.172837495803833),
                    ),
                ),
                Cell(
                    content="11/05/2020",
                    column_index=3,
                    column_span=1,
                    row_index=2,
                    row_span=1,
                    polygon=(
                        Point(x=0.48359203338623047, y=0.15962623059749603),
                        Point(x=0.7029663920402527, y=0.1596541404724121),
                        Point(x=0.7029706835746765, y=0.1728910207748413),
                        Point(x=0.4835953712463379, y=0.1728632003068924),
                    ),
                ),
                Cell(
                    content="11/05/2020",
                    column_index=4,
                    column_span=1,
                    row_index=2,
                    row_span=1,
                    polygon=(
                        Point(x=0.7029663920402527, y=0.1596541404724121),
                        Point(x=0.8904386758804321, y=0.15967799723148346),
                        Point(x=0.8904438018798828, y=0.1729148030281067),
                        Point(x=0.7029706835746765, y=0.1728910207748413),
                    ),
                ),
            ),
        ),
    ),
    paragraphs=(
        Paragraph(
            id_=EntityId(page_2_paragraph_ids[0]),
            order=2,
            content="9176 Riverside Drive\nPanama City, FL 32404",
            polygon=(
                Point(x=0.26941001415252686, y=0.2504948377609253),
                Point(x=0.423315167427063, y=0.2504948377609253),
                Point(x=0.423315167427063, y=0.2758837342262268),
                Point(x=0.26941001415252686, y=0.2758837342262268),
            ),
            confidence=0.999166,
            lines=(
                Line(
                    order=0,
                    content="9176 Riverside Drive",
                    polygon=(
                        Point(x=0.2694302797317505, y=0.2504948377609253),
                        Point(x=0.40402382612228394, y=0.25051161646842957),
                        Point(x=0.4040258526802063, y=0.2594677209854126),
                        Point(x=0.2694318890571594, y=0.2594509720802307),
                    ),
                    confidence=0.999460,
                    words=(
                        Word(
                            order=0,
                            content="9176",
                            confidence=0.999794,
                            polygon=(
                                Point(x=0.2694302797317505, y=0.25054770708084106),
                                Point(x=0.30089136958122253, y=0.25055164098739624),
                                Point(x=0.30089303851127625, y=0.25929388403892517),
                                Point(x=0.26943185925483704, y=0.25928995013237),
                            ),
                            style=Style(
                                background_color="white",
                                color="black",
                                bold=True,
                                italic=True,
                                handwritten=False,
                                font_type="Calibri",
                                font_size="14pt",
                                underlined=False,
                                strikeout=False,
                                subscript=False,
                                superscript=False,
                                smallcaps=False,
                            ),
                        ),
                    ),
                    selection_marks=(
                        SelectionMark(
                            order=1,
                            state="Riverside",
                            confidence=0.998963,
                            polygon=(
                                Point(x=0.3053155839443207, y=0.25051772594451904),
                                Point(x=0.3658568859100342, y=0.25052526593208313),
                                Point(x=0.365858793258667, y=0.25946298241615295),
                                Point(x=0.30531731247901917, y=0.25945544242858887),
                            ),
                        ),
                    ),
                    barcodes=(
                        Barcode(
                            order=2,
                            value="Drive",
                            kind="PRINTED",
                            confidence=0.999622,
                            polygon=(
                                Point(x=0.36990389227867126, y=0.2505073547363281),
                                Point(x=0.40402382612228394, y=0.25051161646842957),
                                Point(x=0.4040258526802063, y=0.2594553828239441),
                                Point(x=0.36990582942962646, y=0.25945112109184265),
                            ),
                        ),
                    ),
                ),
                Line(
                    order=1,
                    content="Panama City, FL 32404",
                    polygon=(
                        Point(x=0.26941001415252686, y=0.2648240923881531),
                        Point(x=0.42331260442733765, y=0.264843225479126),
                        Point(x=0.423315167427063, y=0.2758837342262268),
                        Point(x=0.26941201090812683, y=0.2758646607398987),
                    ),
                    confidence=0.999166,
                    words=(
                        Word(
                            order=0,
                            content="Panama",
                            confidence=0.998021,
                            polygon=(
                                Point(x=0.26941004395484924, y=0.2650187313556671),
                                Point(x=0.3219573497772217, y=0.26502525806427),
                                Point(x=0.32195907831192017, y=0.27371323108673096),
                                Point(x=0.2694116234779358, y=0.27370673418045044),
                            ),
                            style=Style(
                                background_color="white",
                                color="black",
                                bold=True,
                                italic=False,
                                handwritten=False,
                                font_type="Abadi",
                                underlined=False,
                                strikeout=False,
                                subscript=False,
                                superscript=False,
                                smallcaps=False,
                            ),
                        ),
                    ),
                    formulas=(
                        Formula(
                            order=1,
                            value="City",
                            kind="PRINTED",
                            confidence=0.999260,
                            polygon=(
                                Point(x=0.3257099986076355, y=0.2648310959339142),
                                Point(x=0.3551834523677826, y=0.26483476161956787),
                                Point(x=0.35518577694892883, y=0.2758753001689911),
                                Point(x=0.3257122039794922, y=0.2758716642856598),
                            ),
                        ),
                        Formula(
                            order=3,
                            value="32404",
                            kind="PRINTED",
                            confidence=0.999831,
                            polygon=(
                                Point(x=0.37964770197868347, y=0.2648410499095917),
                                Point(x=0.42331260442733765, y=0.26484647393226624),
                                Point(x=0.4233146607875824, y=0.2737540304660797),
                                Point(x=0.37964963912963867, y=0.27374860644340515),
                            ),
                        ),
                    ),
                    signatures=(
                        Signature(
                            order=2,
                            value="FL",
                            confidence=0.999553,
                            polygon=(
                                Point(x=0.35978731513023376, y=0.2650178074836731),
                                Point(x=0.3755180537700653, y=0.2650197744369507),
                                Point(x=0.37551993131637573, y=0.2736184000968933),
                                Point(x=0.3597891330718994, y=0.2736164331436157),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),
)

page_1_only_images = Page(
    id_=EntityId(page1_id),
    page_number=1,
    parsing_type=ParsingType.AWS_TEXTRACT,
    dimension=Dimension(width=1000, height=1000, unit="px"),
    languages=(Language(language_code="eng", confidence=1.0),),
    file_path=file_path1,
    transformations=Transformations(
        thresholding=Thresholding(low_value=2, high_value=2, flag=2),
        blurring=Blurring(kernel=(2, 2), sigma=1.0),
    ),
    images=(
        Image(
            id_=EntityId(page_1_images_ids[0]),
            order=0,
            title=image_title1,
            file_path=image_file_path1,
            polygon=(
                Point(x=0.1, y=0.1),
                Point(x=0.3, y=0.1),
                Point(x=0.3, y=0.3),
                Point(x=0.1, y=0.3),
            ),
        ),
    ),
)

page_2_only_tables = Page(
    id_=EntityId(page2_id),
    page_number=2,
    parsing_type=ParsingType.AWS_TEXTRACT,
    dimension=Dimension(width=1005, height=1005, unit="px"),
    languages=(Language(language_code="eng", confidence=1.0),),
    file_path=file_path2,
    transformations=Transformations(thresholding=Thresholding(low_value=3, high_value=3, flag=1)),
    tables=(
        Table(
            id_=EntityId(page_2_table_ids[0]),
            order=1,
            column_count=4,
            row_count=2,
            polygon=(
                Point(x=0.11592782288789749, y=0.14602451026439667),
                Point(x=0.8904334306716919, y=0.14612334966659546),
                Point(x=0.8904438018798828, y=0.1729148030281067),
                Point(x=0.11593133211135864, y=0.17281654477119446),
            ),
            confidence=0.815917,
            cells=(
                Cell(
                    content="AIRWAY BILL NO.",
                    column_index=1,
                    column_span=1,
                    row_index=1,
                    row_span=1,
                    polygon=(
                        Point(x=0.11592782288789749, y=0.14602451026439667),
                        Point(x=0.28105443716049194, y=0.14604558050632477),
                        Point(x=0.2810569405555725, y=0.15960046648979187),
                        Point(x=0.11592959612607956, y=0.15957945585250854),
                    ),
                    kind="COLUMN_HEADER",
                ),
                Cell(
                    content="INVOICE NO.",
                    column_index=2,
                    column_span=1,
                    row_index=1,
                    row_span=1,
                    polygon=(
                        Point(x=0.28105443716049194, y=0.14604558050632477),
                        Point(x=0.4835886061191559, y=0.1460714340209961),
                        Point(x=0.48359203338623047, y=0.15962623059749603),
                        Point(x=0.2810569405555725, y=0.15960046648979187),
                    ),
                    kind="COLUMN_HEADER",
                ),
                Cell(
                    content="INVOICE DATE",
                    column_index=3,
                    column_span=1,
                    row_index=1,
                    row_span=1,
                    polygon=(
                        Point(x=0.4835886061191559, y=0.1460714340209961),
                        Point(x=0.7029619812965393, y=0.14609943330287933),
                        Point(x=0.7029663920402527, y=0.1596541404724121),
                        Point(x=0.48359203338623047, y=0.15962623059749603),
                    ),
                    kind="COLUMN_HEADER",
                ),
                Cell(
                    content="DATE OF EXPORT",
                    column_index=4,
                    column_span=1,
                    row_index=1,
                    row_span=1,
                    polygon=(
                        Point(x=0.7029619812965393, y=0.14609943330287933),
                        Point(x=0.8904334306716919, y=0.14612334966659546),
                        Point(x=0.8904386758804321, y=0.15967799723148346),
                        Point(x=0.7029663920402527, y=0.1596541404724121),
                    ),
                    kind="COLUMN_HEADER",
                ),
                Cell(
                    content="000231",
                    column_index=1,
                    column_span=1,
                    row_index=2,
                    row_span=1,
                    polygon=(
                        Point(x=0.11592959612607956, y=0.15957945585250854),
                        Point(x=0.2810569405555725, y=0.15960046648979187),
                        Point(x=0.2810593843460083, y=0.172837495803833),
                        Point(x=0.11593133211135864, y=0.17281654477119446),
                    ),
                ),
                Cell(
                    content="000562",
                    column_index=2,
                    column_span=1,
                    row_index=2,
                    row_span=1,
                    polygon=(
                        Point(x=0.2810569405555725, y=0.15960046648979187),
                        Point(x=0.48359203338623047, y=0.15962623059749603),
                        Point(x=0.4835953712463379, y=0.1728632003068924),
                        Point(x=0.2810593843460083, y=0.172837495803833),
                    ),
                ),
                Cell(
                    content="11/05/2020",
                    column_index=3,
                    column_span=1,
                    row_index=2,
                    row_span=1,
                    polygon=(
                        Point(x=0.48359203338623047, y=0.15962623059749603),
                        Point(x=0.7029663920402527, y=0.1596541404724121),
                        Point(x=0.7029706835746765, y=0.1728910207748413),
                        Point(x=0.4835953712463379, y=0.1728632003068924),
                    ),
                ),
                Cell(
                    content="11/05/2020",
                    column_index=4,
                    column_span=1,
                    row_index=2,
                    row_span=1,
                    polygon=(
                        Point(x=0.7029663920402527, y=0.1596541404724121),
                        Point(x=0.8904386758804321, y=0.15967799723148346),
                        Point(x=0.8904438018798828, y=0.1729148030281067),
                        Point(x=0.7029706835746765, y=0.1728910207748413),
                    ),
                ),
            ),
        ),
    ),
)

merged_table = MergedTable(
    parsing_type=ParsingType.AWS_TEXTRACT,
    tables=[
        TableReference.from_raw({"page_number": 1, "table_id": page_1_table_ids[0]}),
        TableReference.from_raw({"page_number": 2, "table_id": page_2_table_ids[0]}),
    ],
)

document_layout = DocumentLayout(
    id_=EntityId(document_layout_id),
    tenant_id=TenantId(tenant_id),
    parsing_features=parsing_features,
    merged_tables={ParsingType.AWS_TEXTRACT: [merged_table]},
    pages=[
        page_1_with_images_kv_pairs_tables_paragraphs,
        page_2_with_images_kv_pairs_tables_paragraphs,
    ],
)

document_layout_short_pages = DocumentLayout(
    id_=EntityId(document_layout_id),
    tenant_id=TenantId(tenant_id),
    parsing_features=parsing_features,
    pages=[
        page_1_only_images,
        page_2_only_tables,
    ],
)

document_layout_2 = DocumentLayout(
    id_=EntityId(uuid4().hex),
    tenant_id=TenantId(tenant_id),
    parsing_features=parsing_features,
    pages=[
        Page(
            id_=EntityId(uuid4().hex),
            page_number=1,
            parsing_type=ParsingType.AZURE_FORM_RECOGNIZER,
            dimension=Dimension(width=1000, height=1000, unit="px"),
            languages=(Language(language_code="by", confidence=1.0),),
            file_path=uuid4().hex,
            transformations=Transformations(
                thresholding=Thresholding(low_value=2, high_value=2, flag=2),
                blurring=Blurring(kernel=(2, 2), sigma=1.0),
            ),
            images=(
                Image(
                    id_=EntityId(page_1_images_ids[0]),
                    order=0,
                    title="TITLE_" + uuid4().hex,
                    file_path="PATH_" + uuid4().hex,
                    polygon=(
                        Point(x=0.1, y=0.1),
                        Point(x=0.3, y=0.1),
                        Point(x=0.3, y=0.3),
                        Point(x=0.1, y=0.3),
                    ),
                ),
            ),
        )
    ],
)

document_layout_user_defined = DocumentLayout(
    id_=EntityId(document_layout_id),
    tenant_id=TenantId(tenant_id),
    parsing_features={ParsingType.USER_DEFINED: {ParsingFeature.TEXT, ParsingFeature.KEY_VALUE_PAIRS}},
    pages=[
        Page(
            id_=EntityId(page1_id),
            page_number=1,
            parsing_type=ParsingType.USER_DEFINED,
            dimension=Dimension(width=1000, height=1000, unit="px"),
            languages=(Language(language_code="eng", confidence=1.0),),
            file_path=file_path1,
            transformations=Transformations(
                thresholding=Thresholding(low_value=2, high_value=2, flag=2),
                blurring=Blurring(kernel=(2, 2), sigma=1.0),
            ),
            images=(
                Image(
                    id_=EntityId(page_1_images_ids[0]),
                    order=0,
                    title=image_title1,
                    file_path=image_file_path1,
                    polygon=(
                        Point(x=0.1, y=0.1),
                        Point(x=0.3, y=0.1),
                        Point(x=0.3, y=0.3),
                        Point(x=0.1, y=0.3),
                    ),
                ),
            ),
        ),
        Page(
            id_=EntityId(page2_id),
            page_number=1,
            parsing_type=ParsingType.AWS_TEXTRACT,
            dimension=Dimension(width=1005, height=1005, unit="px"),
            languages=(Language(language_code="eng", confidence=1.0),),
            file_path=file_path2,
            transformations=Transformations(
                thresholding=Thresholding(low_value=2, high_value=2, flag=2),
                blurring=Blurring(kernel=(2, 2), sigma=1.0),
            ),
            images=(
                Image(
                    id_=EntityId(page_2_table_ids[0]),
                    order=0,
                    title=image_title1,
                    file_path=image_file_path2,
                    polygon=(
                        Point(x=0.1, y=0.1),
                        Point(x=0.3, y=0.1),
                        Point(x=0.3, y=0.3),
                        Point(x=0.1, y=0.3),
                    ),
                ),
            ),
        ),
    ],
)

document_layout_user_defined_2 = DocumentLayout(
    id_=EntityId(document_layout_id),
    tenant_id=TenantId(tenant_id),
    parsing_features={ParsingType.USER_DEFINED: {ParsingFeature.TEXT, ParsingFeature.KEY_VALUE_PAIRS}},
    pages=[
        Page(
            id_=EntityId(page2_id),
            page_number=1,
            parsing_type=ParsingType.USER_DEFINED,
            dimension=Dimension(width=1005, height=1005, unit="px"),
            languages=(Language(language_code="eng", confidence=1.0),),
            file_path=file_path2,
            transformations=Transformations(
                thresholding=Thresholding(low_value=2, high_value=2, flag=2),
                blurring=Blurring(kernel=(2, 2), sigma=1.0),
            ),
            images=(
                Image(
                    id_=EntityId(page_2_table_ids[0]),
                    order=0,
                    title=image_title1,
                    file_path=image_file_path2,
                    polygon=(
                        Point(x=0.1, y=0.1),
                        Point(x=0.3, y=0.1),
                        Point(x=0.3, y=0.3),
                        Point(x=0.1, y=0.3),
                    ),
                ),
            ),
        )
    ],
)


document_layout_dict = {
    "documentLayoutId": "e44f842e3f0c4b62afb076156446f5ec",
    "parsingFeatures": {"AZURE_FORM_RECOGNIZER": ["tables", "images"]},
    "mergedTables": {
        "AWS_TEXTRACT": [
            {
                "parsingType": "AWS_TEXTRACT",
                "tables": [
                    {"pageNumber": 1, "tableId": page_1_table_ids[0]},
                    {"pageNumber": 2, "tableId": page_2_table_ids[0]},
                ],
            },
        ],
    },
    "pages": [
        {
            "id": "a70200f10b65443b97a393f40c1e54c2",
            "groups": [{"id": group_1_id, "name": "Page1 Group", "members": group_1_members}],
            "pageNumber": 1,
            "parsingType": "AWS_TEXTRACT",
            "dimension": {"width": 1000, "height": 1000, "unit": "px"},
            "languages": [{"languageCode": "eng", "confidence": 1.0}],
            "filePath": "ecf5d37bf4944ff7b290670b523652dc",
            "transformations": {
                "thresholding": {"lowValue": 2, "highValue": 2, "flag": 2},
                "blurring": {"kernel": [2, 2], "sigma": 1.0},
                "grayscaling": False,
                "orientation": None,
                "angle": None,
            },
            "images": [
                {
                    "id": page_1_images_ids[0],
                    "order": 0,
                    "title": "06b52904738a475791f7eecd1db4f685",
                    "filePath": "8833fdb9d36544e0b0d153008b74aea8",
                    "polygon": [
                        {"x": 0.1, "y": 0.1},
                        {"x": 0.3, "y": 0.1},
                        {"x": 0.3, "y": 0.3},
                        {"x": 0.1, "y": 0.3},
                    ],
                    "description": image_description,
                }
            ],
            "paragraphs": [
                {
                    "id": page_1_paragraph_ids[0],
                    "order": 2,
                    "content": "VALDOSTA LOWNDES COUNTY\nIndustrial Authority",
                    "confidence": 0.953004,
                    "role": "HEADER",
                    "polygon": [
                        {"x": 0.12720482051372528, "y": 0.06185947731137276},
                        {"x": 0.45422646403312683, "y": 0.06185947731137276},
                        {"x": 0.45422646403312683, "y": 0.104300357401371},
                        {"x": 0.12720482051372528, "y": 0.104300357401371},
                    ],
                    "lines": [
                        {
                            "order": 0,
                            "content": "VALDOSTA LOWNDES COUNTY",
                            "confidence": 0.953004,
                            "polygon": [
                                {"x": 0.16565455496311188, "y": 0.06168489530682564},
                                {"x": 0.4166678488254547, "y": 0.06185947731137276},
                                {"x": 0.4166451096534729, "y": 0.07296974211931229},
                                {"x": 0.16563330590724945, "y": 0.07279309630393982},
                            ],
                            "words": [
                                {
                                    "order": 0,
                                    "confidence": 0.972114,
                                    "polygon": [
                                        {"x": 0.16565382480621338, "y": 0.06206876039505005},
                                        {"x": 0.2470325380563736, "y": 0.06212538108229637},
                                        {"x": 0.24701187014579773, "y": 0.07268821448087692},
                                        {"x": 0.16563360393047333, "y": 0.07263095676898956},
                                    ],
                                    "content": "VALDOSTA",
                                    "style": {
                                        "backgroundColor": "white",
                                        "color": "black",
                                        "bold": True,
                                        "italic": True,
                                        "handwritten": False,
                                        "fontType": "Calibri",
                                        "fontSize": "14pt",
                                        "underlined": False,
                                        "strikeout": False,
                                        "subscript": False,
                                        "superscript": False,
                                        "smallcaps": True,
                                    },
                                },
                                {
                                    "order": 1,
                                    "confidence": 0.897392,
                                    "polygon": [
                                        {"x": 0.26604604721069336, "y": 0.06175471842288971},
                                        {"x": 0.3445536196231842, "y": 0.061809320002794266},
                                        {"x": 0.34453144669532776, "y": 0.07284170389175415},
                                        {"x": 0.2660243511199951, "y": 0.07278646528720856},
                                    ],
                                    "content": "LOWNDES",
                                    "style": {
                                        "backgroundColor": "white",
                                        "color": "black",
                                        "bold": True,
                                        "italic": True,
                                        "handwritten": False,
                                        "fontType": "Calibri",
                                        "fontSize": "14pt",
                                        "underlined": False,
                                        "strikeout": False,
                                        "subscript": False,
                                        "superscript": False,
                                        "smallcaps": True,
                                    },
                                },
                                {
                                    "order": 2,
                                    "confidence": 0.989505,
                                    "polygon": [
                                        {"x": 0.3487030565738678, "y": 0.06196937710046768},
                                        {"x": 0.41666755080223083, "y": 0.06201665475964546},
                                        {"x": 0.4166451096534729, "y": 0.07296974211931229},
                                        {"x": 0.3486810326576233, "y": 0.07292190939188004},
                                    ],
                                    "content": "COUNTY",
                                    "style": {
                                        "backgroundColor": "white",
                                        "color": "black",
                                        "bold": True,
                                        "italic": True,
                                        "handwritten": False,
                                        "fontType": "Calibri",
                                        "fontSize": "14pt",
                                        "underlined": False,
                                        "strikeout": False,
                                        "subscript": False,
                                        "superscript": False,
                                        "smallcaps": True,
                                    },
                                },
                            ],
                            "selectionMarks": [],
                            "barcodes": [],
                            "formulas": [],
                            "signatures": [],
                        },
                        {
                            "order": 1,
                            "content": "Industrial Authority",
                            "confidence": 0.99947,
                            "polygon": [
                                {"x": 0.12726040184497833, "y": 0.0746949315071106},
                                {"x": 0.45422646403312683, "y": 0.0749254897236824},
                                {"x": 0.4541656970977783, "y": 0.104300357401371},
                                {"x": 0.12720482051372528, "y": 0.10406270623207092},
                            ],
                            "words": [
                                {
                                    "order": 0,
                                    "confidence": 0.999091,
                                    "polygon": [
                                        {"x": 0.12726040184497833, "y": 0.0746949315071106},
                                        {"x": 0.2879866063594818, "y": 0.074808269739151},
                                        {"x": 0.2879401743412018, "y": 0.09826946258544922},
                                        {"x": 0.12721601128578186, "y": 0.09815333783626556},
                                    ],
                                    "content": "Industrial",
                                    "style": {
                                        "backgroundColor": "white",
                                        "color": "black",
                                        "bold": True,
                                        "italic": False,
                                        "handwritten": False,
                                        "fontType": "Abadi",
                                        "fontSize": "14pt",
                                        "underlined": False,
                                        "strikeout": False,
                                        "subscript": False,
                                        "superscript": False,
                                        "smallcaps": False,
                                    },
                                },
                                {
                                    "order": 1,
                                    "confidence": 0.99985,
                                    "polygon": [
                                        {"x": 0.29450589418411255, "y": 0.07486402243375778},
                                        {"x": 0.4542263448238373, "y": 0.07497665286064148},
                                        {"x": 0.4541656970977783, "y": 0.104300357401371},
                                        {"x": 0.29444774985313416, "y": 0.10418426245450974},
                                    ],
                                    "content": "Authority",
                                    "style": {
                                        "backgroundColor": "white",
                                        "color": "black",
                                        "bold": True,
                                        "italic": False,
                                        "handwritten": False,
                                        "fontType": "Abadi",
                                        "fontSize": None,
                                        "underlined": False,
                                        "strikeout": False,
                                        "subscript": False,
                                        "superscript": False,
                                        "smallcaps": False,
                                    },
                                },
                            ],
                            "selectionMarks": [],
                            "barcodes": [],
                            "formulas": [],
                            "signatures": [],
                        },
                    ],
                }
            ],
            "tables": [
                {
                    "id": page_1_table_ids[0],
                    "order": 1,
                    "confidence": 0.975097,
                    "columnCount": 4,
                    "rowCount": 2,
                    "polygon": [
                        {"x": 0.09854213893413544, "y": 0.3893252909183502},
                        {"x": 0.9805532693862915, "y": 0.39015230536460876},
                        {"x": 0.9804075956344604, "y": 0.4520988464355469},
                        {"x": 0.09842590242624283, "y": 0.4512314796447754},
                    ],
                    "cells": [
                        {
                            "paragraphId": None,
                            "content": "EVENT",
                            "columnIndex": 1,
                            "columnSpan": 1,
                            "rowIndex": 1,
                            "rowSpan": 1,
                            "kind": "COLUMN_HEADER",
                            "polygon": [
                                {"x": 0.09854213893413544, "y": 0.3893252909183502},
                                {"x": 0.9805532693862915, "y": 0.39015230536460876},
                                {"x": 0.9804075956344604, "y": 0.4520988464355469},
                                {"x": 0.09842590242624283, "y": 0.4512314796447754},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "DATE",
                            "columnIndex": 2,
                            "columnSpan": 1,
                            "rowIndex": 1,
                            "rowSpan": 1,
                            "kind": "COLUMN_HEADER",
                            "polygon": [
                                {"x": 0.3996262550354004, "y": 0.38960760831832886},
                                {"x": 0.6569868326187134, "y": 0.389848917722702},
                                {"x": 0.6569215059280396, "y": 0.41985729336738586},
                                {"x": 0.39956507086753845, "y": 0.41961026191711426},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "LOCATION",
                            "columnIndex": 3,
                            "columnSpan": 1,
                            "rowIndex": 1,
                            "rowSpan": 1,
                            "kind": "COLUMN_HEADER",
                            "polygon": [
                                {"x": 0.6569868326187134, "y": 0.389848917722702},
                                {"x": 0.8123155832290649, "y": 0.3899945616722107},
                                {"x": 0.8122477531433105, "y": 0.4200063645839691},
                                {"x": 0.6569215059280396, "y": 0.41985729336738586},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "DUE DATE",
                            "columnIndex": 4,
                            "columnSpan": 1,
                            "rowIndex": 1,
                            "rowSpan": 1,
                            "kind": "COLUMN_HEADER",
                            "polygon": [
                                {"x": 0.8123155832290649, "y": 0.3899945616722107},
                                {"x": 0.9805532693862915, "y": 0.39015230536460876},
                                {"x": 0.9804826378822327, "y": 0.42016786336898804},
                                {"x": 0.8122477531433105, "y": 0.4200063645839691},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "",
                            "columnIndex": 1,
                            "columnSpan": 1,
                            "rowIndex": 2,
                            "rowSpan": 1,
                            "kind": None,
                            "polygon": [
                                {"x": 0.09848581999540329, "y": 0.41932129859924316},
                                {"x": 0.39956507086753845, "y": 0.41961026191711426},
                                {"x": 0.3994999825954437, "y": 0.45152756571769714},
                                {"x": 0.09842590242624283, "y": 0.4512314796447754},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "April 14, 2011",
                            "columnIndex": 2,
                            "columnSpan": 1,
                            "rowIndex": 2,
                            "rowSpan": 1,
                            "kind": None,
                            "polygon": [
                                {"x": 0.39956507086753845, "y": 0.41961026191711426},
                                {"x": 0.6569215059280396, "y": 0.41985729336738586},
                                {"x": 0.6568519473075867, "y": 0.45178064703941345},
                                {"x": 0.3994999825954437, "y": 0.45152756571769714},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "Valdosta, Georgia",
                            "columnIndex": 3,
                            "columnSpan": 1,
                            "rowIndex": 2,
                            "rowSpan": 1,
                            "kind": None,
                            "polygon": [
                                {"x": 0.6569215059280396, "y": 0.41985729336738586},
                                {"x": 0.8122477531433105, "y": 0.4200063645839691},
                                {"x": 0.8121755719184875, "y": 0.4519333839416504},
                                {"x": 0.6568519473075867, "y": 0.45178064703941345},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "Due upon receipt of documents",
                            "columnIndex": 4,
                            "columnSpan": 1,
                            "rowIndex": 2,
                            "rowSpan": 1,
                            "kind": None,
                            "polygon": [
                                {"x": 0.8122477531433105, "y": 0.4200063645839691},
                                {"x": 0.9804826378822327, "y": 0.42016786336898804},
                                {"x": 0.9804075956344604, "y": 0.4520988464355469},
                                {"x": 0.8121755719184875, "y": 0.4519333839416504},
                            ],
                        },
                    ],
                }
            ],
            "keyValuePairs": [
                {
                    "id": page_1_kvps_ids[0],
                    "key": {
                        "paragraphId": None,
                        "content": "Balance",
                        "polygon": [
                            {"x": 0.7792459726333618, "y": 0.7385748624801636},
                            {"x": 0.8397561311721802, "y": 0.7386471629142761},
                            {"x": 0.8397284746170044, "y": 0.750789225101471},
                            {"x": 0.7792187333106995, "y": 0.7507163286209106},
                        ],
                    },
                    "value": {
                        "paragraphId": None,
                        "content": "$ 125.09",
                        "polygon": [
                            {"x": 0.8828075528144836, "y": 0.7378674745559692},
                            {"x": 0.9610974192619324, "y": 0.7379609942436218},
                            {"x": 0.9610683917999268, "y": 0.7503637075424194},
                            {"x": 0.882779061794281, "y": 0.7502694725990295},
                        ],
                    },
                    "confidence": 0.99925,
                    "order": 0,
                },
                {
                    "id": page_1_kvps_ids[1],
                    "key": {
                        "paragraphId": None,
                        "content": "Signature:",
                        "polygon": [
                            {"x": 0.09872318059206009, "y": 0.8909910917282104},
                            {"x": 0.16686254739761353, "y": 0.8910802602767944},
                            {"x": 0.16683751344680786, "y": 0.9041547775268555},
                            {"x": 0.09869863092899323, "y": 0.904064953327179},
                        ],
                    },
                    "value": None,
                    "confidence": 0.916803,
                    "order": 1,
                },
            ],
        },
        {
            "id": "f361997ff51f4827b7dda192973fb93a",
            "groups": [{"id": group_2_id, "name": "Page2 Group", "members": group_2_members}],
            "pageNumber": 2,
            "parsingType": "AWS_TEXTRACT",
            "dimension": {"width": 1005, "height": 1005, "unit": "px"},
            "languages": [{"languageCode": "eng", "confidence": 1.0}],
            "filePath": "2fb9e0ebd9674250824e1cbb1c2c80e8",
            "transformations": {
                "thresholding": {"lowValue": 3, "highValue": 3, "flag": 1},
                "blurring": None,
                "grayscaling": False,
                "orientation": None,
                "angle": None,
            },
            "images": [
                {
                    "id": page_2_images_ids[0],
                    "order": 0,
                    "title": None,
                    "filePath": "fb00d04bf4a643938a91ad2bbaad9111",
                    "polygon": [
                        {"x": 0.2, "y": 0.2},
                        {"x": 0.4, "y": 0.2},
                        {"x": 0.4, "y": 0.4},
                        {"x": 0.2, "y": 0.4},
                    ],
                    "description": None,
                }
            ],
            "paragraphs": [
                {
                    "id": page_2_paragraph_ids[0],
                    "order": 2,
                    "content": "9176 Riverside Drive\nPanama City, FL 32404",
                    "confidence": 0.999166,
                    "role": None,
                    "polygon": [
                        {"x": 0.26941001415252686, "y": 0.2504948377609253},
                        {"x": 0.423315167427063, "y": 0.2504948377609253},
                        {"x": 0.423315167427063, "y": 0.2758837342262268},
                        {"x": 0.26941001415252686, "y": 0.2758837342262268},
                    ],
                    "lines": [
                        {
                            "order": 0,
                            "content": "9176 Riverside Drive",
                            "confidence": 0.99946,
                            "polygon": [
                                {"x": 0.2694302797317505, "y": 0.2504948377609253},
                                {"x": 0.40402382612228394, "y": 0.25051161646842957},
                                {"x": 0.4040258526802063, "y": 0.2594677209854126},
                                {"x": 0.2694318890571594, "y": 0.2594509720802307},
                            ],
                            "words": [
                                {
                                    "order": 0,
                                    "confidence": 0.999794,
                                    "polygon": [
                                        {"x": 0.2694302797317505, "y": 0.25054770708084106},
                                        {"x": 0.30089136958122253, "y": 0.25055164098739624},
                                        {"x": 0.30089303851127625, "y": 0.25929388403892517},
                                        {"x": 0.26943185925483704, "y": 0.25928995013237},
                                    ],
                                    "content": "9176",
                                    "style": {
                                        "backgroundColor": "white",
                                        "color": "black",
                                        "bold": True,
                                        "italic": True,
                                        "handwritten": False,
                                        "fontType": "Calibri",
                                        "fontSize": "14pt",
                                        "underlined": False,
                                        "strikeout": False,
                                        "subscript": False,
                                        "superscript": False,
                                        "smallcaps": False,
                                    },
                                }
                            ],
                            "selectionMarks": [
                                {
                                    "order": 1,
                                    "confidence": 0.998963,
                                    "polygon": [
                                        {"x": 0.3053155839443207, "y": 0.25051772594451904},
                                        {"x": 0.3658568859100342, "y": 0.25052526593208313},
                                        {"x": 0.365858793258667, "y": 0.25946298241615295},
                                        {"x": 0.30531731247901917, "y": 0.25945544242858887},
                                    ],
                                    "state": "Riverside",
                                }
                            ],
                            "barcodes": [
                                {
                                    "order": 2,
                                    "confidence": 0.999622,
                                    "polygon": [
                                        {"x": 0.36990389227867126, "y": 0.2505073547363281},
                                        {"x": 0.40402382612228394, "y": 0.25051161646842957},
                                        {"x": 0.4040258526802063, "y": 0.2594553828239441},
                                        {"x": 0.36990582942962646, "y": 0.25945112109184265},
                                    ],
                                    "value": "Drive",
                                    "kind": "PRINTED",
                                }
                            ],
                            "formulas": [],
                            "signatures": [],
                        },
                        {
                            "order": 1,
                            "content": "Panama City, FL 32404",
                            "confidence": 0.999166,
                            "polygon": [
                                {"x": 0.26941001415252686, "y": 0.2648240923881531},
                                {"x": 0.42331260442733765, "y": 0.264843225479126},
                                {"x": 0.423315167427063, "y": 0.2758837342262268},
                                {"x": 0.26941201090812683, "y": 0.2758646607398987},
                            ],
                            "words": [
                                {
                                    "order": 0,
                                    "confidence": 0.998021,
                                    "polygon": [
                                        {"x": 0.26941004395484924, "y": 0.2650187313556671},
                                        {"x": 0.3219573497772217, "y": 0.26502525806427},
                                        {"x": 0.32195907831192017, "y": 0.27371323108673096},
                                        {"x": 0.2694116234779358, "y": 0.27370673418045044},
                                    ],
                                    "content": "Panama",
                                    "style": {
                                        "backgroundColor": "white",
                                        "color": "black",
                                        "bold": True,
                                        "italic": False,
                                        "handwritten": False,
                                        "fontType": "Abadi",
                                        "fontSize": None,
                                        "underlined": False,
                                        "strikeout": False,
                                        "subscript": False,
                                        "superscript": False,
                                        "smallcaps": False,
                                    },
                                }
                            ],
                            "selectionMarks": [],
                            "barcodes": [],
                            "formulas": [
                                {
                                    "order": 1,
                                    "confidence": 0.99926,
                                    "polygon": [
                                        {"x": 0.3257099986076355, "y": 0.2648310959339142},
                                        {"x": 0.3551834523677826, "y": 0.26483476161956787},
                                        {"x": 0.35518577694892883, "y": 0.2758753001689911},
                                        {"x": 0.3257122039794922, "y": 0.2758716642856598},
                                    ],
                                    "value": "City",
                                    "kind": "PRINTED",
                                },
                                {
                                    "order": 3,
                                    "confidence": 0.999831,
                                    "polygon": [
                                        {"x": 0.37964770197868347, "y": 0.2648410499095917},
                                        {"x": 0.42331260442733765, "y": 0.26484647393226624},
                                        {"x": 0.4233146607875824, "y": 0.2737540304660797},
                                        {"x": 0.37964963912963867, "y": 0.27374860644340515},
                                    ],
                                    "value": "32404",
                                    "kind": "PRINTED",
                                },
                            ],
                            "signatures": [
                                {
                                    "order": 2,
                                    "confidence": 0.999553,
                                    "polygon": [
                                        {"x": 0.35978731513023376, "y": 0.2650178074836731},
                                        {"x": 0.3755180537700653, "y": 0.2650197744369507},
                                        {"x": 0.37551993131637573, "y": 0.2736184000968933},
                                        {"x": 0.3597891330718994, "y": 0.2736164331436157},
                                    ],
                                    "value": "FL",
                                }
                            ],
                        },
                    ],
                }
            ],
            "tables": [
                {
                    "id": page_2_table_ids[0],
                    "order": 1,
                    "confidence": 0.815917,
                    "columnCount": 4,
                    "rowCount": 2,
                    "polygon": [
                        {"x": 0.11592782288789749, "y": 0.14602451026439667},
                        {"x": 0.8904334306716919, "y": 0.14612334966659546},
                        {"x": 0.8904438018798828, "y": 0.1729148030281067},
                        {"x": 0.11593133211135864, "y": 0.17281654477119446},
                    ],
                    "cells": [
                        {
                            "paragraphId": None,
                            "content": "AIRWAY BILL NO.",
                            "columnIndex": 1,
                            "columnSpan": 1,
                            "rowIndex": 1,
                            "rowSpan": 1,
                            "kind": "COLUMN_HEADER",
                            "polygon": [
                                {"x": 0.11592782288789749, "y": 0.14602451026439667},
                                {"x": 0.28105443716049194, "y": 0.14604558050632477},
                                {"x": 0.2810569405555725, "y": 0.15960046648979187},
                                {"x": 0.11592959612607956, "y": 0.15957945585250854},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "INVOICE NO.",
                            "columnIndex": 2,
                            "columnSpan": 1,
                            "rowIndex": 1,
                            "rowSpan": 1,
                            "kind": "COLUMN_HEADER",
                            "polygon": [
                                {"x": 0.28105443716049194, "y": 0.14604558050632477},
                                {"x": 0.4835886061191559, "y": 0.1460714340209961},
                                {"x": 0.48359203338623047, "y": 0.15962623059749603},
                                {"x": 0.2810569405555725, "y": 0.15960046648979187},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "INVOICE DATE",
                            "columnIndex": 3,
                            "columnSpan": 1,
                            "rowIndex": 1,
                            "rowSpan": 1,
                            "kind": "COLUMN_HEADER",
                            "polygon": [
                                {"x": 0.4835886061191559, "y": 0.1460714340209961},
                                {"x": 0.7029619812965393, "y": 0.14609943330287933},
                                {"x": 0.7029663920402527, "y": 0.1596541404724121},
                                {"x": 0.48359203338623047, "y": 0.15962623059749603},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "DATE OF EXPORT",
                            "columnIndex": 4,
                            "columnSpan": 1,
                            "rowIndex": 1,
                            "rowSpan": 1,
                            "kind": "COLUMN_HEADER",
                            "polygon": [
                                {"x": 0.7029619812965393, "y": 0.14609943330287933},
                                {"x": 0.8904334306716919, "y": 0.14612334966659546},
                                {"x": 0.8904386758804321, "y": 0.15967799723148346},
                                {"x": 0.7029663920402527, "y": 0.1596541404724121},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "000231",
                            "columnIndex": 1,
                            "columnSpan": 1,
                            "rowIndex": 2,
                            "rowSpan": 1,
                            "kind": None,
                            "polygon": [
                                {"x": 0.11592959612607956, "y": 0.15957945585250854},
                                {"x": 0.2810569405555725, "y": 0.15960046648979187},
                                {"x": 0.2810593843460083, "y": 0.172837495803833},
                                {"x": 0.11593133211135864, "y": 0.17281654477119446},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "000562",
                            "columnIndex": 2,
                            "columnSpan": 1,
                            "rowIndex": 2,
                            "rowSpan": 1,
                            "kind": None,
                            "polygon": [
                                {"x": 0.2810569405555725, "y": 0.15960046648979187},
                                {"x": 0.48359203338623047, "y": 0.15962623059749603},
                                {"x": 0.4835953712463379, "y": 0.1728632003068924},
                                {"x": 0.2810593843460083, "y": 0.172837495803833},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "11/05/2020",
                            "columnIndex": 3,
                            "columnSpan": 1,
                            "rowIndex": 2,
                            "rowSpan": 1,
                            "kind": None,
                            "polygon": [
                                {"x": 0.48359203338623047, "y": 0.15962623059749603},
                                {"x": 0.7029663920402527, "y": 0.1596541404724121},
                                {"x": 0.7029706835746765, "y": 0.1728910207748413},
                                {"x": 0.4835953712463379, "y": 0.1728632003068924},
                            ],
                        },
                        {
                            "paragraphId": None,
                            "content": "11/05/2020",
                            "columnIndex": 4,
                            "columnSpan": 1,
                            "rowIndex": 2,
                            "rowSpan": 1,
                            "kind": None,
                            "polygon": [
                                {"x": 0.7029663920402527, "y": 0.1596541404724121},
                                {"x": 0.8904386758804321, "y": 0.15967799723148346},
                                {"x": 0.8904438018798828, "y": 0.1729148030281067},
                                {"x": 0.7029706835746765, "y": 0.1728910207748413},
                            ],
                        },
                    ],
                }
            ],
            "keyValuePairs": [
                {
                    "id": page_2_kvps_ids[0],
                    "key": {
                        "paragraphId": None,
                        "content": "AIRWAY BILL NO.",
                        "polygon": [
                            {"x": 0.11943134665489197, "y": 0.1489686369895935},
                            {"x": 0.21852388978004456, "y": 0.1489812731742859},
                            {"x": 0.21852533519268036, "y": 0.15784229338169098},
                            {"x": 0.11943251639604568, "y": 0.1578296720981598},
                        ],
                    },
                    "value": {
                        "paragraphId": None,
                        "content": "000231",
                        "polygon": [
                            {"x": 0.1181400939822197, "y": 0.16277551651000977},
                            {"x": 0.16564106941223145, "y": 0.16278156638145447},
                            {"x": 0.1656423807144165, "y": 0.17165611684322357},
                            {"x": 0.11814125627279282, "y": 0.17165008187294006},
                        ],
                    },
                    "confidence": 0.933754,
                    "order": 0,
                },
                {
                    "id": page_2_kvps_ids[1],
                    "key": {
                        "paragraphId": None,
                        "content": "EMAIL",
                        "polygon": [
                            {"x": 0.5561466217041016, "y": 0.33884578943252563},
                            {"x": 0.592820405960083, "y": 0.3388502895832062},
                            {"x": 0.5928229689598083, "y": 0.34754979610443115},
                            {"x": 0.5561490058898926, "y": 0.347545325756073},
                        ],
                    },
                    "value": {
                        "paragraphId": None,
                        "content": "",
                        "polygon": [
                            {"x": 0.7116237282752991, "y": 0.3391474485397339},
                            {"x": 0.8342684507369995, "y": 0.3391624093055725},
                            {"x": 0.8342725038528442, "y": 0.3502322733402252},
                            {"x": 0.7116273641586304, "y": 0.350217342376709},
                        ],
                    },
                    "confidence": 0.930332,
                    "order": 1,
                },
            ],
        },
    ],
}
