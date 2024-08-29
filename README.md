telegram-notification.py
    a custom script to parse wazuh json alert and then send the alert to telegram chat. this script read argument alert, chat id and token.
custom-rule-wazuh.xml
    this custom rule is used to filter file adding & modification from spesific wazuh agent list that listed as "etc/lists/webserver_list". this rule is wazuh file integrity monitor to detect file adding & modification. this rule only monitor file that exist on
    path : /var/www/html, and file extention is ; .php .html .htm .xml .js .css .sh .json .env .lock
custom-ossec.conf
    this is configuration that need to add to the wazuh configuration (ossec.conf) 
