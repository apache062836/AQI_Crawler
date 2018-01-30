#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 22:42:03 2018

@author: David Y. Tseng
"""

from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select


def initialization(browser):
    area   = Select(browser.find_element_by_id('ddl_Area'))
    site   = Select(browser.find_element_by_id('ddl_Site'))
    button = browser.find_element_by_id('btn_Search')
    
    return area, site, button

def aqi_influence(aqi):
    if (aqi.isdigit() and int(aqi) >= 0 and int(aqi) <= 50):
        health_impact = 'Good'
        status        = 'Green'
        
    elif(aqi.isdigit() and int(aqi) >= 51 and int(aqi) <= 100):
        health_impact = 'Moderate'
        status        = 'Yellow'
        
    elif(aqi.isdigit() and int(aqi) >= 101 and int(aqi) <= 150):
        health_impact = 'Unhealthy for Sensitive Groups'
        status        = 'Orange'
        
    elif(aqi.isdigit() and int(aqi) >= 151 and int(aqi) <= 200):
        health_impact = 'Unhealthy'
        status        = 'Red'
    
    elif(aqi.isdigit() and int(aqi) >= 201 and int(aqi) <= 300):
        health_impact = 'Very Unhealthy'
        status        = 'Purple'
        
    elif(aqi.isdigit() and int(aqi) >= 301 and int(aqi) <= 500):
        health_impact = 'Hazardous'
        status        = 'Marnoon'
    
    else:
        health_impact = ' '
        status        = 'Gray'
    
    return health_impact, status

def data_obtaining(browser, area, site, button):
    for area_option in (area.options):
        area_option.click()
        
        all_site_options = site.options
        for s in xrange(len(all_site_options)):
            all_site_options[s].click()
            site_id   = all_site_options[s].get_attribute('value')
            button.click()
            
            soup      = BeautifulSoup(browser.page_source)
            site_name = (soup.find('a', attrs={'class':'SITE_NAME'})).text
            aqi       = (soup.find('h2', attrs={'id':'lb_AQI'})).text
            health_impact, status = aqi_influence(aqi)
            
            print '%s %s %s %s %s' %(site_id, site_name, aqi, health_impact, status)
            
            all_site_options = site.options

def data_time_handler(browser):
    data_time = str((browser.find_element_by_id('lb_DataTime')).text)
    
    while (data_time == '--'):
        data_time = str((browser.find_element_by_id('lb_DataTime')).text)
        
    return datetime.strptime(data_time, '%Y-%m-%d %H:%M:%S')

def main():
    browser = webdriver.Firefox()
    browser.get('https://taqm.epa.gov.tw/taqm/aqi-map.aspx')
    
    data_announced_time = data_time_handler(browser)
    print data_announced_time
    
    area, site, button = initialization(browser)
    print 'SITE_ID SITE_NAME AQI HEALTH_IMPACT STATUS'
    data_obtaining(browser, area, site, button)
    
    browser.close()

if __name__ == '__main__':
    main()
