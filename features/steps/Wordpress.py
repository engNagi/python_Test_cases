# -- FILE: features/steps/Wordpress.py,

import time
from behave import given, when, then

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

# ----------Variables----------
url = "http://localhost:8888/wordpress/"
AdminUser = "admin"
AdminPass = "!NCS2019"

# Test mit Browser Chrome
driver = webdriver.Chrome()


# Test mit Browser Firefox
# driver = webdriver.Firefox()


# -------------------------------------------
#               G I V E N 
# -------------------------------------------

@given('we have navigated to the given URL')  # for Scenario: WrongUser, WrongPassword, UserLogin
def step_impl(context):
	# Zu der konfigurierten URL gehen
	driver.start_client
	driver.get(url)

	# Überprüfen ob die richtige URL aufgerufen wurde
	assert driver.current_url == url


@given('we are logged in as admin')  # for Scenario: CreateUser
def step_impl(context):
	# Überprüfung ob der Admin eingeloggt ist
	assert driver.current_url == "http://localhost:8888/wordpress/wp-admin/"


@given('we have navigated as ADMIN to the Userlist')  # for Scenario: EditUser, DeleteUser
def step_impl(context):
	# Zu der konfigurierten URL gehen
	driver.start_client
	driver.get(url)

	# Anmelden auf der Webseite klicken -> Anmeldemaske erscheint
	driver.find_element_by_xpath("/html/body/div/div/div/div/aside/section[7]/ul/li[1]/a").click()

	# warte 1 Sekunde
	time.sleep(1)

	# Benutzername eingeben
	driver.find_element_by_xpath("//*[@id='user_login']").send_keys(AdminUser)

	# Passwort eingeben
	driver.find_element_by_xpath("//*[@id='user_pass']").send_keys(AdminPass)

	# Anmelden klicken -> Benutzer wird angemeldet
	driver.find_element_by_xpath("//*[@id='wp-submit']").click()

	# Link zur Benutzerliste klicken
	driver.find_element_by_xpath("//a[@class='wp-has-submenu wp-not-current-submenu menu-top menu-icon-users']").click()

	# Überprüfung ob der Admin auf der Benutzerlistenseite ist
	assert driver.current_url == "http://localhost:8888/wordpress/wp-admin/users.php"


# -------------------------------------------
#               W H E N 
# -------------------------------------------

@when('we click on "Anmelden"')  # for Scenario: WrongUser, WrongPassword, UserLogin
def step_impl(context):
	# Anmelden auf der Webseite klicken -> Anmeldemaske erscheint
	driver.find_element_by_xpath("/html/body/div/div/div/div/aside/section[7]/ul/li[1]/a").click()

	# Ueberpruefung ob die Anmeldemaske erscheint
	assert driver.current_url == "http://localhost:8888/wordpress/wp-login.php"

	# warte 1 Sekunde
	time.sleep(1)


@when('we create the new users')  # for Scenario: CreateUser
def step_impl(context):
	for row in context.table:
		# "Neu hinzufügen" anklicken
		driver.find_element_by_link_text("Neu hinzufügen").click()

		# Benutzername eingeben
		driver.find_element_by_xpath("//*[@id='user_login']").send_keys(row['Benutzername'])

		# Email eingeben
		driver.find_element_by_xpath("//*[@id='email']").send_keys(row['Email'])

		# Vorname eingeben
		driver.find_element_by_xpath("//*[@id='first_name']").send_keys(row['Vorname'])

		# Nachname eingeben
		driver.find_element_by_xpath("//*[@id='last_name']").send_keys(row['Nachname'])

		# auf "Passwort anzeigen" klicken
		driver.find_element_by_xpath("//button[@class='button wp-generate-pw hide-if-no-js'][1]").click()

		# Passwort eingeben
		driver.find_element_by_xpath("//*[@id='pass1-text']").clear()
		driver.find_element_by_xpath("//*[@id='pass1-text']").send_keys(row['Passwort'][0:1])
		driver.find_element_by_xpath("//*[@id='pass1-text']").send_keys(row['Passwort'][1:])

		# Email Benachrichtigung abschalten
		driver.find_element_by_xpath("//*[@id='send_user_notification']").click()

		# Rolle anpassen
		pulldown = Select(driver.find_element_by_xpath("//*[@id='role']"))
		pulldown.select_by_visible_text(row['Rolle'])

		# "Neuen Benutzer hinzufuegen" klicken
		driver.find_element_by_xpath("//*[@id='createusersub']").click()

		# Überprüfung ob der Benutzer angelegt wurde
		assert driver.find_element_by_xpath(
			"//div[@id='message'][1]/p[1]").text == "Neuer Benutzer erstellt. Benutzer bearbeiten"

		# Screenshot erstellen Local
		# driver.save_screenshot('Create_User_%s.png' % row['Benutzername'])

		# Screenshot erstellen Allure
		#allure.attach(driver.get_screenshot_as_png(), name='Create_User_%s.png' % row['Benutzername'],attachment_type=allure.attachment_type.PNG)


@when('we click on the "{Benutzername}"')  # for Scenario: EditUser
def step_impl(context, Benutzername):
	# klicke auf den Benutzername
	driver.find_element_by_link_text(Benutzername).click()


@when('we search for the "{Benutzername}"')  # for Scenario: DeleteUser
def step_impl(context, Benutzername):
	# Suchmaske leeren
	driver.find_element_by_xpath("//*[@id='user-search-input']").clear()

	# Benutzername in Suchmaske eingeben
	driver.find_element_by_xpath("//*[@id='user-search-input']").send_keys(Benutzername)

	# Suche ausführen
	driver.find_element_by_xpath("//*[@id='search-submit']").click()


# -------------------------------------------
#               " A N D " 
# -------------------------------------------

@when('enter the wrong admin login data')  # for Scenario: WrongPassword
def step_impl(context):
	# Benutzername eingeben
	driver.find_element_by_xpath("//*[@id='user_login']").send_keys(AdminUser)

	# flasches Passwort eingeben
	driver.find_element_by_xpath("//*[@id='user_pass']").send_keys("falsch")

	# Anmelden klicken -> Benutzer wird abgelehnt
	driver.find_element_by_xpath("//*[@id='wp-submit']").click()


@when('enter the wrong user login data')  # for Scenario: WrongUser
def step_impl(context):
	# flaschen Benutzername eingeben
	driver.find_element_by_xpath("//*[@id='user_login']").send_keys("FalscherUser")

	# Passwort eingeben
	driver.find_element_by_xpath("//*[@id='user_pass']").send_keys(AdminPass)

	# Anmelden klicken -> Benutzer wird abgelehnt
	driver.find_element_by_xpath("//*[@id='wp-submit']").click()


@when('enter the admin login data')  # for Scenario: AdminLogin
def step_impl(context):
	# Benutzername eingeben
	driver.find_element_by_xpath("//*[@id='user_login']").send_keys(AdminUser)

	# Passwort eingeben
	driver.find_element_by_xpath("//*[@id='user_pass']").send_keys(AdminPass)

	# Anmelden klicken -> Benutzer wird angemeldet
	driver.find_element_by_xpath("//*[@id='wp-submit']").click()


@then('then the Admin logout')  # for Scenario: CreateUser
def step_impl(context):
	# Mouseover in der Admin-Bar um den Logout-Button sichtbar zu machen
	ActionChains(driver).move_to_element(
		driver.find_element_by_xpath("//*[@id='wp-admin-bar-top-secondary']")).perform()

	# warte 1 Sekunde
	time.sleep(1)

	# Abmelden klicken -> Benutzer wird abgemeldet
	driver.find_element_by_xpath("//li[@id='wp-admin-bar-logout'][1]").click()

	# Ueberpruefung ob der Benutzer erfolgreich ausgeloggt wurde
	assert driver.find_element_by_xpath("/html//p[@class='message'][1]").text == "Du hast dich erfolgreich abgemeldet."

	# Scrrenshot erstellen Local
	# driver.save_screenshot('Logout_admin.png')

	# Screenshot erstellen Allure
	#allure.attach(driver.get_screenshot_as_png(), name='Logout_admin.png', attachment_type=#allure.attachment_type.PNG)


@then('the "{Benutzername}" is able to logout')  # for Scenario: UserLogin
def step_impl(context, Benutzername):
	# Abmelden klicken -> Benutzer wird abgemeldet
	driver.find_element_by_xpath("//li[@id='wp-admin-bar-logout'][1]").click()

	# Ueberpruefung ob der Benutzer erfolgreich ausgeloggt wurde
	assert driver.find_element_by_xpath("/html//p[@class='message'][1]").text == "Du hast dich erfolgreich abgemeldet."

	# Scrrenshot erstellen Local
	# driver.save_screenshot('Logout_User_%s.png' % Benutzername)

	# Screenshot erstellen Allure
	#allure.attach(driver.get_screenshot_as_png(), name='Logout_User_%s.png' % Benutzername,attachment_type=allure.attachment_type.PNG)


@given('navigate to the user list')  # for Scenario: CreateUser
def step_impl(context):
	# Mouseover im Dashboard ueber "Benutzer"
	driver.find_element_by_xpath("//a[@class='wp-has-submenu wp-not-current-submenu menu-top menu-icon-users']").click()


@when('enter the users "{Benutzername}" and "{Passwort}"')  # for Scenario: UserLogin
def step_impl(context, Benutzername, Passwort):
	# warte 1 Sekunde
	time.sleep(1)

	# Benutzername eingeben
	driver.find_element_by_xpath("//*[@id='user_login']").send_keys(Benutzername)

	# Passwort eingeben
	driver.find_element_by_xpath("//*[@id='user_pass']").send_keys(Passwort)

	# Anmelden klicken -> Benutzer wird angemeldet
	driver.find_element_by_xpath("//*[@id='wp-submit']").click()


@when('find the "{Benutzername}" in the list')  # for Scenario: DeleteUser
def step_impl(context, Benutzername):
	# Check ob der Benutzer der richtige ist
	assert driver.find_element_by_xpath(
		".//td[@class='username column-username has-row-actions column-primary'][1]/strong").text == Benutzername

	# Screenshot erstellen Local
	# driver.save_screenshot('Search_%s.png' % row['Benutzername'])

	# Screenshot erstellen Allure
	#allure.attach(driver.get_screenshot_as_png(), name='Search_%s.png' % Benutzername,attachment_type=allure.attachment_type.PNG)


@then('the "{Benutzername}" is deleted')  # for Scenario: DeleteUser
def step_impl(context, Benutzername):
	# Überprüfung ob der Benutzer gelöscht wurde
	assert driver.find_element_by_xpath("//div[@id='message']/p").text == "Benutzer gelöscht"

	# Screenshot erstellen Local
	# driver.save_screenshot('Delete_User_%s.png' % row['Benutzername'])

	# Screenshot erstellen Allure
	#allure.attach(driver.get_screenshot_as_png(), name='Delete_User_%s.png' % Benutzername,attachment_type=#allure.attachment_type.PNG)


# -------------------------------------------
#               T H E N 
# -------------------------------------------

@then('the login Password isnt succesfull')  # for Scenario: WrongPassword
def step_impl(context):
	# Ueberpruefung ob der login aufgrund eines flaschen Passwortes abgelehnt wurde
	assert driver.find_element_by_xpath(
		"//*[@id='login_error']").text == \
	       "FEHLER: Das Passwort, das du für den Benutzernamen admin eingegeben hast, ist nicht korrekt. Passwort vergessen?"

	# Screenshot erstellen Local
	# driver.save_screenshot('WrongPassword.png')

	# Screenshot erstellen Allure
	#allure.attach(driver.get_screenshot_as_png(), name='WrongPassword.png', attachment_type=#allure.attachment_type.PNG)


@then('the login User isnt succesfull')  # for Scenario: WrongUser
def step_impl(context):
	# Ueberpruefung ob der login aufgrund eines flaschen Users abgelehnt wurde
	assert driver.find_element_by_xpath(
		"//*[@id='login_error']").text == "FEHLER: Ungültiger Benutzername. Passwort vergessen?"

	# Screenshot erstellen Local
	# driver.save_screenshot('WrongUser.png')

	# Screenshot erstellen Allure
	##allure.attach(driver.get_screenshot_as_png(), name='WrongUser.png', attachment_type=#allure.attachment_type.PNG)


@then('we reach the admin dashboard')  # for Scenario: AdminLogin
def step_impl(context):
	# Ueberpruefung ob der Admin Login erfolgreich war
	assert driver.current_url == "http://localhost:8888/wordpress/wp-admin/"

	# Scrrenshot erstellen Local
	# driver.save_screenshot('AdminDashboard.png')

	# Screenshot erstellen Allure
	#allure.attach(driver.get_screenshot_as_png(), name='AdminDashboard.png', attachment_type=#allure.attachment_type.PNG)


@then('they are added to the list')  # for Scenario: CreateUser
def step_impl(context):
	for row in context.table:
		# Überprüfung ob der Benutzer angelegt wurde
		assert driver.find_element_by_xpath(
			"//div[@id='message'][1]/p[1]").text == "Neuer Benutzer erstellt. Benutzer bearbeiten"

		# Screenshot erstellen Local
		# driver.save_screenshot('Create_User_%s.png' % row['Benutzername'])

		# Screenshot erstellen Allure
		#allure.attach(driver.get_screenshot_as_png(), name='Create_User_%s.png' % row['Benutzername'],attachment_type=#allure.attachment_type.PNG)


@then('we can change the role to "{Rolle}"')  # for Scenario: EditUser
def step_impl(context, Rolle):
	# Rolle anpassen
	pulldown = Select(driver.find_element_by_xpath("//*[@id='role']"))
	pulldown.select_by_visible_text(Rolle)

	# Screenshot erstellen Local
	# driver.save_screenshot('Role_change_%s.png' % Rolle)

	# Screenshot erstellen Allure
	#allure.attach(driver.get_screenshot_as_png(), name='Role_change_%s.png' % Rolle,attachment_type=#allure.attachment_type.PNG)

	# warte 1 Sekunde
	time.sleep(1)

	# "Benutzer aktualisieren" klicken
	driver.find_element_by_xpath("//*[@id='submit']").click()

	# Überprüfung ob die aktualisierung durchgeführt wurde
	assert driver.find_element_by_xpath("//*[@id='message']/p[1]/strong").text == "Benutzer aktualisiert."

	# Screenshot erstellen Local
	# driver.save_screenshot('Role_change_commit_%s.png' % Rolle)

	# Screenshot erstellen Allure
	#allure.attach(driver.get_screenshot_as_png(), name='Role_change_commit_%s.png' % Rolle,	              attachment_type=#allure.attachment_type.PNG)

	# zur Benutzerliste zurück gelangen
	driver.find_element_by_xpath("//*[@id='menu-users']/a/div[2]").click()


@then('we can change the "{Farbschema}"')  # for Scenario: EditUser
def step_impl(context, Farbschema):
	# Farbschema auf Standart ändern
	if Farbschema == "Standart":
		driver.find_element_by_xpath("//*[@id='color-picker']/div[1]").click()

	# Farbschema auf Hell ändern
	if Farbschema == "Hell":
		driver.find_element_by_xpath("//*[@id='color-picker']/div[2]").click()

	# Farbschema auf Blau ändern
	if Farbschema == "Balu":
		driver.find_element_by_xpath("//*[@id='color-picker']/div[3]").click()

	# Farbschema auf Kaffee ändern
	if Farbschema == "Kaffee":
		driver.find_element_by_xpath("//*[@id='color-picker']/div[4]").click()

	# Farbschema auf Ektoplasma ändern
	if Farbschema == "Ektoplasma":
		driver.find_element_by_xpath("//*[@id='color-picker']/div[5]").click()

	# Farbschema auf Mitternacht ändern
	if Farbschema == "Mitternacht":
		driver.find_element_by_xpath("//*[@id='color-picker']/div[6]").click()

	# Farbschema auf Meer ändern
	if Farbschema == "Meer":
		driver.find_element_by_xpath("//*[@id='color-picker']/div[7]").click()

	# Farbschema auf Hell ändern
	if Farbschema == "Sonnenaufgang":
		driver.find_element_by_xpath("//*[@id='color-picker']/div[8]").click()

	# Screenshot erstellen Local
	# driver.save_screenshot('Color_change_%s.png' % Rolle)

	# Screenshot erstellen Allure
	#allure.attach(driver.get_screenshot_as_png(), name='Color_change_%s.png' % Farbschema,	              attachment_type=#allure.attachment_type.PNG)

	# warte 1 Sekunde
	time.sleep(1)

	# "Benutzer aktualisieren" klicken
	driver.find_element_by_xpath("//*[@id='submit']").click()

	# Überprüfung ob die aktualisierung durchgeführt wurde
	assert driver.find_element_by_xpath("//*[@id='message']/p[1]/strong").text == "Benutzer aktualisiert."

	# Screenshot erstellen Local
	# driver.save_screenshot('Color_change_commit_%s.png' % Farbschema)

	# Screenshot erstellen Allure
	#allure.attach(driver.get_screenshot_as_png(), name='Color_change_commit_%s.png' % Farbschema,	              attachment_type=#allure.attachment_type.PNG)

	# zur Benutzerliste zurück gelangen
	driver.find_element_by_xpath("//*[@id='menu-users']/a/div[2]").click()


@then('the "{Benutzername}" should be logged in')  # for Scenario: UserLogin
def step_impl(context, Benutzername):
	# Mouseover in der Admin-Bar um den Logout-Button sichtbar zu machen
	ActionChains(driver).move_to_element(
		driver.find_element_by_xpath("//*[@id='wp-admin-bar-top-secondary']")).perform()

	# warte 1 Sekunde
	time.sleep(1)

	# Überprüfen ob der Benutzer eingelogt ist
	assert driver.find_element_by_xpath("//li[@id='wp-admin-bar-user-info'][1]").text.split()[2] == Benutzername

	# Screenshot erstellen Local
	# driver.save_screenshot('Logged_in_%s.png' % Benutzername)

	# Screenshot erstellen Allure
	#allure.attach(driver.get_screenshot_as_png(), name='Logged_in_%s.png' % Benutzername,	              attachment_type=#allure.attachment_type.PNG)


@then('we can click on delete button')  # for Scenario: DeleteUser
def step_impl(context):
	# Mouseover in der Admin-Bar um den Logout-Button sichtbar zu machen
	ActionChains(driver).move_to_element(driver.find_element_by_xpath(
		".//td[@class='username column-username has-row-actions column-primary'][1]/strong")).perform()

	# warte 1 Sekunde
	time.sleep(1)

	# auf löschen klicken
	driver.find_element_by_xpath(
		"//tr/td[@class='username column-username has-row-actions column-primary']/div/span[@class='delete']").click()

	# ggf. "Den gesamten Inhalt löschen" auswählen
	try:
		driver.find_element_by_xpath("//*[@id='delete_option0']").click()
	except:
		print("")

	# löschen bestätigen
	driver.find_element_by_xpath("//*[@id='submit']").click()
