from puppyblog import FlaskForm,StringField,PasswordField,SubmitField,\
    ValidationError,DataRequired,EqualTo,FileField,FileAllowed,current_user, Email, SelectField
from puppyblog.users.models import Users


class LoginForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',
                                                                           message="Oops! Passwords must match")])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    sex = SelectField("Sex", choices=[('m', 'Male'), ('f', 'Female'),('t','Trans')],validators=[DataRequired()])
    mobile = StringField('Number', validators=[DataRequired()])
    country_code = SelectField("Country Code",choices=[('91',"IN(+91)"),(1,"US(+1)"), (213,"DZ(+213)"), (376,"AD(+376)"),
                                                       (244,"AO(+244)"), (1264,"AI(+1264)"), (1268,"AG(+1268)"),
                                                       (54,"AR(+54)"), (374,"AM(+374)"), (297,"AW(+297)"),
                                                       (61,"AU(+61)"), (43,"AT(+43)"), (994,"AZ(+994)"),
                                                       (1242,"BS(+1242)"), (973,"BH(+973)"), (880,"BD(+880)"),
                                                       (1246,"BB(+1246)"), (375,"BY(+375)"), (32,"BE(+32)"),
                                                       (501,"BZ(+501)"), (229,"BJ(+229)"), (1441,"BM(+1441)"),
                                                       (975,"BT(+975)"), (591,"BO(+591)"), (387,"BA(+387)"),
                                                       (267,"BW(+267)"), (55,"BR(+55)"), (673,"BN(+673)"),
                                                       (359,"BG(+359)"), (226,"BF(+226)"), (257,"BI(+257)"),
                                                       (855,"KH(+855)"), (237,"CM(+237)"), (1,"CA(+1)"),
                                                       (238,"CV(+238)"), (1345,"KY(+1345)"), (236,"CF(+236)"),
                                                       (56,"CL(+56)"), (86,"CN(+86)"), (57,"CO(+57)"),
                                                       (269,"KM(+269)"), (242,"CG(+242)"), (682,"CK(+682)"),
                                                       (506,"CR(+506)"), (385,"HR(+385)"), (53,"CU(+53)"),
                                                       (9039,"CY(+90392"), (357,"CY(+357)"), (42,"CZ(+42)"),
                                                       (45,"DK(+45)"), (253,"DJ(+253)"), (1809,"DM(+1809)"),
                                                       (1809,"DO(+1809)"), (593,"EC(+593)"), (20,"EG(+20)"),
                                                       (503,"SV(+503)"), (240,"GQ(+240)"), (291,"ER(+291)"),
                                                       (372,"EE(+372)"), (251,"ET(+251)"), (500,"FK(+500)"),
                                                       (298,"FO(+298)"), (679,"FJ(+679)"), (358,"FI(+358)"),
                                                       (33,"FR(+33)"), (594,"GF(+594)"), (689,"PF(+689)"),
                                                       (241,"GA(+241)"), (220,"GM(+220)"), (7880,"GE(+7880)"),
                                                       (49,"DE(+49)"), (233,"GH(+233)"), (350,"GI(+350)"),
                                                       (30,"GR(+30)"), (299,"GL(+299)"), (1473,"GD(+1473)"),
                                                       (590,"GP(+590)"), (671,"GU(+671)"), (502,"GT(+502)"),
                                                       (224,"GN(+224)"), (245,"GW(+245)"), (592,"GY(+592)"),
                                                       (509,"HT(+509)"), (504,"HN(+504)"), (852,"HK(+852)"),
                                                       (36,"HU(+36)"), (354,"IS(+354)"), (62,"ID(+62)"),
                                                       (98,"IR(+98)"), (964,"IQ(+964)"), (353,"IE(+353)"),
                                                       (972,"IL(+972)"), (39,"IT(+39)"), (1876,"JM(+1876)"),
                                                       (81,"JP(+81)"), (962,"JO(+962)"), (7,"KZ(+7)"),
                                                       (254,"KE(+254)"), (686,"KI(+686)"), (850,"KP(+850)"),
                                                       (82,"KR(+82)"), (965,"KW(+965)"), (996,"KG(+996)"),
                                                       (856,"LA(+856)"), (371,"LV(+371)"), (961,"LB(+961)"),
                                                       (266,"LS(+266)"), (231,"LR(+231)"), (218,"LY(+218)"),
                                                       (417,"LI(+417)"), (370,"LT(+370)"), (352,"LU(+352)"),
                                                       (853,"MO(+853)"), (389,"MK(+389)"), (261,"MG(+261)"),
                                                       (265,"MW(+265)"), (60,"MY(+60)"), (960,"MV(+960)"),
                                                       (223,"ML(+223)"), (356,"MT(+356)"), (692,"MH(+692)"),
                                                       (596,"MQ(+596)"), (222,"MR(+222)"), (269,"YT(+269)"),
                                                       (52,"MX(+52)"), (691,"FM(+691)"), (373,"MD(+373)"),
                                                       (377,"MC(+377)"), (976,"MN(+976)"), (1664,"MS(+1664)"),
                                                       (212,"MA(+212)"), (258,"MZ(+258)"), (95,"MN(+95)"),
                                                       (264,"NA(+264)"), (674,"NR(+674)"), (977,"NP(+977)"),
                                                       (31,"NL(+31)"), (687,"NC(+687)"), (64,"NZ(+64)"),
                                                       (505,"NI(+505)"), (227,"NE(+227)"), (234,"NG(+234)"),
                                                       (683,"NU(+683)"), (672,"NF(+672)"), (670,"NP(+670)"),
                                                       (47,"NO(+47)"), (968,"OM(+968)"), (680,"PW(+680)"),
                                                       (507,"PA(+507)"), (675,"PG(+675)"), (595,"PY(+595)"),
                                                       (51,"PE(+51)"), (63,"PH(+63)"), (48,"PL(+48)"),
                                                       (351,"PT(+351)"), (1787,"PR(+1787)"), (974,"QA(+974)"),
                                                       (262,"RE(+262)"), (40,"RO(+40)"), (7,"RU(+7)"),
                                                       (250,"RW(+250)"), (378,"SM(+378)"), (239,"ST(+239)"),
                                                       (966,"SA(+966)"), (221,"SN(+221)"), (381,"CS(+381)"),
                                                       (248,"SC(+248)"), (232,"SL(+232)"), (65,"SG(+65)"),
                                                       (421,"SK(+421)"), (386,"SI(+386)"), (677,"SB(+677)"),
                                                       (252,"SO(+252)"), (27,"ZA(+27)"), (34,"ES(+34)"),
                                                       (94,"LK(+94)"), (290,"SH(+290)"), (1869,"KN(+1869)"),
                                                       (1758,"SC(+1758)"), (249,"SD(+249)"), (597,"SR(+597)"),
                                                       (268,"SZ(+268)"), (46,"SE(+46)"), (41,"CH(+41)"),
                                                       (963,"SI(+963)"), (886,"TW(+886)"), (7,"TJ(+7)"),
                                                       (66,"TH(+66)"), (228,"TG(+228)"), (676,"TO(+676)"),
                                                       (1868,"TT(+1868)"), (216,"TN(+216)"), (90,"TR(+90)"),
                                                       (7,"TM(+7)"), (993,"TM(+993)"), (1649,"TC(+1649)"),
                                                       (688,"TV(+688)"), (256,"UG(+256)"), (380,"UA(+380)"),
                                                       (971,"AE(+971)"), (598,"UY(+598)"), (7,"UZ(+7)"),
                                                       (678,"VU(+678)"), (379,"VA(+379)"), (58,"VE(+58)"),
                                                       (84,"VN(+84)"), (1284,"VG(+84)"), (1340,"VI(+84)"),
                                                       (681,"WF(+681)"), (969,"YE(+969)"), (967,"YE(+967)"),
                                                       (260,"ZM(+260)"), (263,"ZW(+263)"), (44,"GB(+44)")],
                               validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self,field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')

    def check_username(self,field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('Your username is taken!')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture.The format can be uploaded is .jpg,.jpeg,.png',validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Update')

    def check_email(self,field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')

    def check_username(self,field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('Your username is taken!')