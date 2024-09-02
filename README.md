1. telegram-notification.py :
   	a custom script to parse wazuh json alert and then send the alert to telegram chat. this script read argument alert, chat id and token. Put the script under "/var/ossec/integration" folder, don't forget to change the file ownership to 'wazuh' and the chmod +x
    
3. custom-rule-wazuh.xml :
	this custom rule is used to filter file adding & modification from spesific wazuh agent list that listed as "etc/lists/webserver_list". this rule is based on wazuh file integrity monitor to detect file adding & modification. it depend on wazuh rule number 550 & 554. this rule only monitor file that exist on path "/var/www/html", and the file extention is ; .php .html .htm .xml .js .css .sh .json .env .lock
    
3. custom-ossec.conf :
   	this is configuration that need to add to the wazuh configuration (ossec.conf). you have to add the telegram chat id and API token on this configuration.

You Are Free to use & modify the script
