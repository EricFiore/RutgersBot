import xml.etree.ElementTree as ET
import requests
import sys


class RouteData:
    def __init__(self):
        self.rte = self.__init_rte_list()
        self.stp = self.__store_stops(self.rte)

    def __init_rte_list(self):
        url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=rutgers'
        xml_data = self.__rtrv_web_data(url)
        with open('routeList', 'wb') as file:
            file.write(xml_data.content)
        file.close()
        tree = ET.parse('routeList')
        root = tree.getroot()
        route_dict = dict()
        for child in root.findall('route'):
            title, tag = (child.get('title'), child.get('tag'))
            route_dict.update({title:tag})
        del tree
        del root
        return route_dict

    def __store_stops(self, dictionary):
        stop_dict = dict()
        for tag in dictionary.values():
            url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=rutgers&r=' + tag
            xml_data = self.__rtrv_web_data(url)
            file_name = tag + 'stopList'
            with open(file_name, 'wb') as stop_file:
                stop_file.write(xml_data.content)
            stop_file.close()
            stop_dict.update({tag:self.__retreive_stops(file_name)})
        return stop_dict

    def __retreive_stops(self, file_name):
        stop_tree = ET.parse(file_name)
        stop_root = stop_tree.getroot()
        line_st_dict = dict()
        for child in stop_root.findall('route'):
            for grandchild in child.findall('stop'):
                title, tag = (grandchild.get('title'), grandchild.get('tag'))
                line_st_dict.update({title:tag})
        return line_st_dict

    def __rtrv_web_data(self, url):
        try:
            xml_response = requests.get(url, timeout=3)
            xml_response.raise_for_status()
        except requests.exceptions.HTTPError as httperr:
            print("http error", httperr)
            sys.exit(1)
        except requests.exceptions.ConnectionError as conerr:
            print('connection error', conerr)
            sys.exit(1)
        except requests.exceptions.Timeout as timeerr:
            print("timeout error", timeerr)
            sys.exit(1)
        return xml_response