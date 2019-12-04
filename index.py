import requests
import locale
import xml.etree.ElementTree as ET
import os

from setup import get_qb_url
from requests import session as sessionStart
from setup import get_base_file_url, get_login_session_info, get_login_url, get_qb_databases_id

def getAllRecords(db_ID, despliegue):

	url = get_qb_url() + db_ID;

	with open('./queries/GetRecords', 'r') as file:
		headers = { 'Content-Type': 'application/xml', 'QUICKBASE-ACTION': 'API_DoQuery' };
		data = file.read();
		data = data.replace("{query}", despliegue);
		
		#TIcket is a temporary token valid for 6 months RENEW
		#Check app token i don't remember if it's temporary
		response = requests.post(url, headers = headers, data = data)
		return response.content;

def updateRecord(db_ID, rid, fields):
	url = get_qb_url() + db_ID;
	headers = { 'Content-Type': 'application/xml', 'QUICKBASE-ACTION': 'API_EditRecord' };
	with open('EditRecords', 'r') as file:
		data = file.read();
		data = data.replace("{rid}", rid);
		stringFields = "";
		for fieldName in fields:
			stringFields += '<field name="{}">{}</field>\n'.format(fieldName, fields[fieldName])
		data = data.replace("{fields}", stringFields);

		response = requests.post(url, headers = headers,
			#TIcket is a temporary token valid for 6 months RENEW
			#Check app token i don't remember if it's temporary
			data = data
		)
		return response.content;

def getFile(dbID, recordID, fieldNumber):

	fileUrl = get_base_file_url() + dbID + '/a/r' + recordID + '/e' + str(fieldNumber) + '/v0';

	session = requests.session();
	session.post(get_login_url(), data = get_login_session_info());

	response = session.get(fileUrl, stream = True)

	return response.content;

def saveFile(folder, fileBytes, filename):
	dir = "./files/" + folder
	fileLocation = dir + "/" + filename;
	try:
		if not os.path.exists(dir):
			os.mkdir(dir)
		f = open(fileLocation, "wb+")
		f.write(fileBytes);
		f.close();
		return folder + "/" + filename;
	except Exception as e:
		pass;

def checkForLinks(record):
	asBuilt = record.find("link_listado_direcciones").text;
	listado = record.find("link_asbuilt").text;
	diseno = record.find("link_plano_diseno").text;
	checklist = record.find("link_checklist").text;
	certificacion = record.find("link_certificacion").text;

	if (asBuilt != None):
		return True;
	if (listado != None):
		return True;
	if (diseno != None):
		return True;
	if (checklist != None):
		return True;
	if (certificacion != None):
		return True;


nombreDespliegue = "Despliegue Linares"
nombreProyecto = "EZENTIS"
url = "10.0.1.27/";

dbID = get_qb_databases_id()[nombreProyecto];
records = getAllRecords(dbID, nombreDespliegue);
xmlRoot = ET.fromstring(records);

for record in xmlRoot.findall('record'):

	recordID = record.attrib['rid'];
	identificador = record.find("identificador").text;
	asBuilt = record.find("asbuilt").text;
	listado = record.find("listado_direcciones").text;
	diseno = record.find("diseno").text;
	checklist = record.find("checklist").text;
	certificacion = record.find("certificacion").text;

	update_list = {};

	if (checkForLinks(record)):
		continue;

	if (asBuilt != None):
		asBuiltFile = getFile(dbID, recordID, 37);
		filename = "{}_As_Built_{}.dwg".format(identificador, nombreProyecto);
		asBuiltLocation = saveFile(nombreDespliegue, asBuiltFile, filename);
		update_list.update({ "link_asbuilt": url + asBuiltLocation });

	if (listado != None):
		listadoFile = getFile(dbID, recordID, 38);
		_, file_extension = os.path.splitext(listado)
		filename = "{}_Cert_Numero_{}{}".format(identificador, nombreProyecto, file_extension);
		listadoLocation = saveFile(nombreDespliegue, listadoFile, filename);
		update_list.update({ "link_listado_direcciones": url + listadoLocation });

	if (diseno != None):
		disenoFile = getFile(dbID, recordID, 36);
		_, file_extension = os.path.splitext(diseno)
		filename = "{}_Plano_Diseno_{}{}".format(identificador, nombreProyecto, file_extension);
		disenoLocation = saveFile(nombreDespliegue, disenoFile, filename);
		update_list.update({ "link_plano_diseno": url + disenoLocation });

	if (checklist != None):
		checklistFile = getFile(dbID, recordID, 39);
		_, file_extension = os.path.splitext(checklist)
		filename = "{}_Check_Construccion_{}{}".format(identificador, nombreProyecto, file_extension);
		checklistLocation = saveFile(nombreDespliegue, checklistFile, filename);
		update_list.update({ "link_checklist": url + checklistLocation });

	if (certificacion != None):
		certificacionFile = getFile(dbID, recordID, 39);
		_, file_extension = os.path.splitext(certificacion)
		filename = "{}_Check_Certificacion_{}{}".format(identificador, nombreProyecto, file_extension);
		certificacionLocation = saveFile(nombreDespliegue, certificacionFile, filename);
		update_list.update({ "link_certificacion": url + certificacionLocation });

	if (update_list == {}):
		continue;

	print("Processed Record: " + recordID + " Identificador: " + identificador);

	updateRecord(dbID, recordID, update_list);