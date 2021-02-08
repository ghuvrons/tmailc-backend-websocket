import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s [%(levelname)s]: %(message)s")

from RCloneDrive import RCloneDrive

token = """{"access_token":"ya29.a0AfH6SMCFHmqK31TCAPrQfIag5PCu3lqSqMBwtG6IVxd7my7BLM5T7Q32w41uEWUzPFlkfozsHaVbkVHd-TWzJr39GNKckU-M-mSyQks0ntfbaxm482NJCY4cXIOuRNoX-YHj2I3K1fTmJ9nuw8DnvXsW1wNUR4XD6r6oInSkLOg","token_type":"Bearer","refresh_token":"1//0gVahorUwA8iECgYIARAAGBASNwF-L9Irsh0aw-f9XKcSNDb9aBq3aD-IVqwZbggfjXuEub62ZuvZtZ-Y2ZUjkJJRYEPNDDW3MqM","expiry":"2021-02-03T00:12:07.278985254Z"}"""
# token = """token = {"access_token":"ya29.A0AfH6SMB7SaaJRdJ34Fkka7c-62L4pCl9xK5AbHFoD2CbVF9AZqrf8TAGTQIS6U6S3sEgQZ3sbj1z6SUM76-AL_qCIocH8DfA6BaAQEhjUM7bTQSNNm0zZIOK6FhPE2BvrT0BAT8w2_DXp1E_scxNBhQMa2onqnxNnC_5STRqWfQ","token_type":"Bearer","refresh_token":"1//0g00zx6Mb8CvECgYIARAAGBASNwF-L9IrSM61q_ZacMuA5MPmRhU63gjicFwgvfsNmGeYkfMWZIkIkf75RSdimHWk93APOkcgFmY","expiry":"2020-11-12T09:22:03.523627578Z"}"""
folder_id = "1yKmbE5JLJL-AY9sWh3_dXm9HhR_UDqZT"


try:
    rCloneDrive = RCloneDrive(token)
    result = rCloneDrive.copy( 
            folder_id, 
            "/root/cpebr_server/tmailc-backend-websocket/localhost/Service/tes"
    )
    print(result)
except Exception as e:
    print(e)