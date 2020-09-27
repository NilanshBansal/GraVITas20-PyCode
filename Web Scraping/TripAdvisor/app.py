from datetime import datetime
start_time = datetime.now()
print(start_time)
import operator
from configfile import *


def random_proxy():
    return random.randint(0, len(https_proxies) - 1)


offset = '30'
pages = '4'

for i in range(int(pages)):
    try:
        https_proxies = requests.get('http://list.didsoft.com/get?email=kedarmanedb@gmail.com&pass=4xkxre&pid=httppremium&showcountry=no&https=yes',timeout=20,verify=False).text.split('\n')[:3500]
    except:
        try:
            https_proxies = requests.get('http://list.didsoft.com/get?email=kedarmanedb@gmail.com&pass=4xkxre&pid=httppremium&showcountry=no&https=yes',timeout=20,verify=False).text.split('\n')[:-1]
        except:
            pass

    sleep(random.random())

    url = 'https://www.tripadvisor.in/RestaurantSearch?Action=PAGE&geo=186338&ajax=0&sortOrder=alphabetical&o=a{}&availSearchEnabled=false'.format(offset)

    idx = 0
    for attempt in range(100):
        idx = random_proxy()
        print('PROXY IS 1 : ',https_proxies[idx])
        print(url)
        try:
            res = requests.get(url,headers=html_headers,proxies={'https': https_proxies[idx]},timeout=5,verify=False)
            soup_30 = BeautifulSoup(res.text,"html.parser")
            eatery_div = soup_30.find('div',{'id':'EATERY_SEARCH_RESULTS'})
            anchor_divs = eatery_div.findAll('div',{'class':'listing'})
        except Exception as e:
            print('EXCEPTION AT 38: ')
            #print(str(e))
            del https_proxies[idx]
            continue
        else:
            break
    
    try:
        eatery_div = soup_30.find('div',{'id':'EATERY_SEARCH_RESULTS'})
        anchor_divs = eatery_div.findAll('div',{'class':'listing'})
    except Exception as e:
        print('EXCEPTION AT 49: ')

        with open('individual_rests/49exception.html','w') as f:
            f.write(res.text)

        #print(str(e))
        offset = str(int(offset) + 30)
        continue

    all_res_urls = []
    
    for item in anchor_divs:
        anchor = item.find('a',{'class':'property_title'})
        
        try:
            res_url = anchor['href']
        except:
            try:
                res_url = anchor['data-url']
            except Exception as e:
                print('EXCEPTION AT 66: ')
                #print(str(e))
                continue

        if 'www.' in res_url:
            pass
        else:
            res_url = 'https://www.tripadvisor.in' + res_url

        all_res_urls.append(res_url)

    all_restaurants = []
    count = 0

    for restaurant_url in all_res_urls:
        obj = {}

        count = count + 1
        try:
            res_id = restaurant_url.split('Restaurant_Review-g186338-d')[1].split('-',1)[0]
        except Exception as e:
            print('EXCEPTION AT 83: ')
            #print(str(e))
            continue
        
        obj['s.no'] = count
        obj['url'] = restaurant_url
        obj['res_id'] = res_id

        flag = 0

        for attempt in range(100):
            idx = random_proxy()
            print('PROXY IS 2 : ',https_proxies[idx])
            print(restaurant_url)
            try:
                res = requests.get(restaurant_url,headers=html_headers,proxies={'https': https_proxies[idx]},timeout=5,verify=False)
                new_soup = BeautifulSoup(res.text,"html.parser")
                script_text = new_soup.findAll('script',{'data-rup':'@ta/platform.runtime'})[0].findNext('script').text
            except Exception as e:
                print('EXCEPTION AT 101: ')
                #print(str(e))
                del https_proxies[idx]
                continue
            else:
                flag = 1
                print('----------------------- SUCCESSFUL ----------------------')
                break
        
        if flag == 0:
            print('FLAG IS 0000: ')
            continue

        try:
            script_text = new_soup.findAll('script',{'data-rup':'@ta/platform.runtime'})[0].findNext('script').text
        except Exception as e:
            #print(str(e))
            with open('individual_rests/' + res_id + '.html','w') as f:
                f.write(res.text)
            print('EXCEPTION AT LINE 118')
            continue
        else:
            try:
                res_json = json.loads(script_text.split(' ',1)[1][:-4])
            except Exception as e:
                print('EXCEPTION AT LINE 123')
                #print(str(e))
                continue
            else:
                try:
                    rest_responses = res_json['redux']['api']['responses']
                except Exception as e:
                    print('EXCEPTION AT LINE 129')
                    #print(str(e))
                    continue

        overview_key = '/data/1.0/restaurant/{}/overview'.format(str(res_id))
        location_key = '/data/1.0/location/{}'.format(res_id)

        try:
            location_data = rest_responses[location_key]['data']
        except Exception as e:
            print('EXCEPTION AT 145: ')
            #print(str(e))
            continue
            
        try:
            obj['name'] = location_data['name']
        except:
            obj['name'] = ''
        
        try:
            obj['latitude'] = location_data['latitude']
        except:
            obj['latitude'] = ''

        try:
            obj['longitude'] = location_data['longitude']
        except:
            obj['longitude'] = ''

        try:
            obj['rating'] = location_data['rating']
        except:
            obj['rating'] = ''

        try:
            obj['phone'] = location_data['phone']
        except:
            obj['phone'] = ''

        try:
            obj['official_website'] = location_data['website']
        except:
            obj['official_website'] = ''
        
        try:
            obj['claim_status'] = new_soup.find('div',{'class':'restaurantName'}).find('span').text.strip()
        except:
            obj['claim_status'] = ''

        obj['city'] = 'London'
        obj['country'] = 'United Kingdom'

        try:
            obj['street_name'] = location_data['address_obj']['street1']
        except:
            obj['street_name'] = ''

        try:
            house_nos = re.findall(r'\d+',obj['street_name'])
            if len(house_nos) == 2 and obj['street_name'].find(house_nos[0]+'-') != -1:
                obj['house_no'] = house_nos[0] + '-' + house_nos[1]
            else:
                obj['house_no'] = house_nos[0]
        except:
            obj['house_no'] = ''
        else:
            obj['street_name'] = obj['street_name'].replace(obj['house_no'],'').strip()

        try:
            obj['postcode'] = location_data['address_obj']['postalcode']
        except:
            obj['postcode'] = ''
        
        try:
            working_hours = []
            for item in location_data['display_hours']:
                day = item['days']
                day_hours = item['times']
                day_hours = ", ".join(day_hours)
                working_hours.append(day + " : " + day_hours)
            
            obj['working_hours'] = "; ".join(working_hours)
        except:
            obj['working_hours'] = ''

        
        try:
            overview_data = rest_responses[overview_key]['data']
        except Exception as e:
            print('EXCEPTION AT 219: ')
            #print(str(e))
            continue
            

        try:
            obj['neighbourhood'] = overview_data['location']['neighborhood']
        except:
            obj['neighbourhood'] = ''

        try:
            obj['email'] = overview_data['contact']['email']
        except:
            obj['email'] = ''

        try:
            obj['tripadvisor_rank'] = overview_data['rating']['secondaryRanking']['rank']
        except:
            obj['tripadvisor_rank'] = ''

        try:
            obj['priceRange'] = overview_data['detailCard']['tagTexts']['priceRange']['tags'][0]['tagValue']
            # if obj['priceRange'] == 'Cheap Eats':
            #     obj['priceRange'] = '₹'
            # elif obj['priceRange'] == 'Mid-range':
            #     obj['priceRange'] = '₹₹ - ₹₹₹'
            # elif obj['priceRange'] == 'Fine Dining':
            #     obj['priceRange'] = '₹₹₹₹'
            # else:
            #     pass
        except:
            obj['priceRange'] = ''

        try:
            cuisine_names = []
            for item in overview_data['detailCard']['tagTexts']['cuisines']['tags']:
                cuisine_names.append(item['tagValue'])

            obj['cuisines'] = ', '.join(cuisine_names)

        except:
            obj['cuisines'] = ''


        try:
            special_diet_names = []
            for item in overview_data['detailCard']['tagTexts']['dietary_restrictions']['tags']:
                special_diet_names.append(item['tagValue'])
            
            obj['special_diets'] = ', '.join(special_diet_names)

        except:
            obj['special_diets'] = ''


        try:
            feature_names = []
            for item in overview_data['detailCard']['tagTexts']['features']['tags']:
                feature_names.append(item['tagValue'])
            
            obj['features'] = ', '.join(feature_names)

        except:
            obj['features'] = ''

        try:
            meal_names = []
            for item in overview_data['detailCard']['tagTexts']['meals']['tags']:
                meal_names.append(item['tagValue'])
            
            obj['meals'] = ', '.join(meal_names)

        except:
            obj['meals'] = ''

        all_restaurants.append(obj)

    # print("NO OF RESTAURANTS : ",len(all_restaurants))

    writeHeader=True
    if((os.path.exists('scraped_data/' + str(offset) + '.csv'))):
        writeHeader=False
    
    headlines = ['s.no','res_id','name','claim_status','rating','tripadvisor_rank','priceRange','house_no','street_name','neighbourhood','city','country','postcode','latitude','longitude','phone','email','url','official_website','cuisines','special_diets','features','meals','working_hours']
    with open('scraped_data/' + str(offset) + '.csv', 'w',encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f,headlines)
        if writeHeader:
            writer.writeheader()
        for info in all_restaurants:
            writer.writerow(info)

    offset = str(int(offset)+30)


print(datetime.now()-start_time)