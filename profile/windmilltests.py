from windmill.authoring import WindmillTestClient

def test_login_logout():
    client = WindmillTestClient(__name__)

    client.type(text=u'ivan', id=u'id_username')
    client.click(id=u'id_password')
    client.type(text=u'passwd', id=u'id_password')
    client.click(value=u'\u0412\u043e\u0439\u0442\u0438')
    client.waits.forPageLoad(timeout=u'20000')
    client.waits.forElement(link=u'Exit', timeout=u'8000')
    client.click(link=u'Exit')
    client.waits.forPageLoad(timeout=u'20000')
    
def test_profile_change():
    client = WindmillTestClient(__name__)

    client.click(id=u'id_username')
    client.type(text=u'ivan', id=u'id_username')
    client.type(text=u'passwd', id=u'id_password')
    client.click(value=u'\u0412\u043e\u0439\u0442\u0438')
    client.waits.forPageLoad(timeout=u'20000')
    client.waits.forElement(link=u'Edit profile', timeout=u'8000')
    client.click(link=u'Edit profile')
    client.waits.forPageLoad(timeout=u'20000')
    client.waits.forElement(timeout=u'8000', id=u'id_contacts')
    client.click(id=u'id_contacts')
    client.type(text=u'ivan2@gmail.com', id=u'id_contacts')
    client.click(xpath=u'/html/body/form/p[1]')
    client.click(value=u'\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c')
    client.waits.forPageLoad(timeout=u'20000')
    client.waits.forElement(link=u'Exit', timeout=u'8000')
    client.click(link=u'Exit')
    client.waits.forPageLoad(timeout=u'20000')
    
def test_middleware():
    client = WindmillTestClient(__name__)

    client.click(id=u'id_username')
    client.type(text=u'ivan', id=u'id_username')
    client.type(text=u'passwd', id=u'id_password')
    client.click(value=u'\u0412\u043e\u0439\u0442\u0438')
    client.waits.forPageLoad(timeout=u'20000')
    client.waits.forElement(link=u'+', timeout=u'8000')
    client.click(link=u'+')
    client.click(link=u'Exit')
    client.waits.forPageLoad(timeout=u'20000')
    
def test_template_tag():
    client = WindmillTestClient(__name__)

    client.click(id=u'id_username')
    client.type(text=u'ivan', id=u'id_username')
    client.type(text=u'passwd', id=u'id_password')
    client.click(value=u'\u0412\u043e\u0439\u0442\u0438')
    client.waits.forPageLoad(timeout=u'20000')
    client.waits.forElement(link=u'Edit in admin', timeout=u'8000')
    client.click(link=u'Edit in admin')
    client.waits.forPageLoad(timeout=u'20000')
    client.waits.forElement(xpath=u"//a[@id='calendarlink0']/img", timeout=u'8000')
    client.click(xpath=u"//a[@id='calendarlink0']/img")
    client.click(link=u'<')
    client.click(name=u'_save')
    client.waits.forPageLoad(timeout=u'20000')
    client.waits.forElement(link=u'                                 \u0412\u044b\u0439\u0442\u0438', timeout=u'8000')
    client.click(link=u'                                 \u0412\u044b\u0439\u0442\u0438')
    client.waits.forPageLoad(timeout=u'20000')