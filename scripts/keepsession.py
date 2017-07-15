from opsutils import PagarmeAdmin

pagarme_admin = PagarmeAdmin()
pagarme_admin.load_session_id()
session_id = pagarme_admin.get_session_id()
status = pagarme_admin.test_session_id()
