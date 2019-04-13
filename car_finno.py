# https://www.finn.no/car/used/search.html?dealer_segment=3&engine_fuel=0%2F1&location=20016&price_from=0&price_to=500000&registration_class=1&sort=4

import requests

nrow      = '10000'
priceFrom = '0'
priceTo   = '50000'
kmFrom    = '100000'
kmTo      = '200000'
yearFrom  = '1990'
yearTo    = '2019'
searchInTrondelag = '&location=20016' #leave empty to search everywhere
# add body_type=4 for stationvagon
url       = 'https://www.finn.no/car/used/search.html?'\
            'dealer_segment=3&engine_fuel=0%2F1'+searchInTrondelag+'&'\
            '&mileage_from='+kmFrom+'&mileage_to='+kmTo+'&price_from='+priceFrom+'&price_to='+priceTo+'&'\
            'registration_class=1&sort=4&year_from='+yearFrom+'&year_to='+yearTo+'&sales_form=1&rows='+nrow

response = requests.get(url)

cars = []

s = -1
link  = ''
year  = ''
km    = ''
kr    = ''
name  = ''
maxY  = 0
maxKm = 0
maxKr = 0
tmpCounter = 0
for line in response.iter_lines():
  if line:
    line = line.decode('utf-8')

    if s==-1 and '<div class="ads__unit__content">' in line:
      s = 0
    elif s==0 and 'data-finnkode' in line:
      tag   = 'data-finnkode=\"'
      start = line.find(tag)+len(tag)
      end   = line.find('\n')-1
      t = line[start:end]
      if start==36:
        break
      link = 'http://finn.no/car/used/ad.html?finnkode='+t
      s = 1
    elif (s==1 and 'data-search-resultitem>' in line) or (s==1 and tmpCounter>0):
      if tmpCounter<1:
        tmpCounter += 1
      else:
        name = line[12:len(line)]
        s = 2
        tmpCounter = 0
    elif s==2 and 'ads__unit__content__keys' in line:
      s = 3
    elif s==3:
      tag = '<span>'
      year = int(line[line.find(tag)+len(tag):line.find('</span>')])
      if year > maxY:
        maxY = year
      s = 4
    elif s==4:
      tag = '<span>'
      km = line[line.find(tag)+len(tag):line.find(' km</span>')]
      km = ''.join(km.split())
      km = int(float(km))
      if km > maxKm and km!=12345678 and km!=99999999 and km!=0:
        maxKm = km
      s = 5
    elif s==5:
      tag = '<span>'
      kr = line[line.find(tag)+len(tag):line.find(' kr</span>')]
      kr = ''.join(kr.split())
      kr = int(float(kr))
      if kr > maxKr:
        maxKr = kr      

      if km!=12345678 and km!=99999999 and km!=0:
        cars.append([link, name, year, km, kr])

      s = -1

minR = 10.0
maxR = -1.0
best = ''
worst = ''
cars2 = []
for i in cars:
  year = i[2]
  km = i[3]
  kr = i[4]

  yi = maxY/year-1
  kmi = km/maxKm
  kri = kr/maxKr
  r = yi + kmi + kri

  v = (i[0],i[2],i[3],i[4],r,i[1])
  cars2.append(v)

  if r > maxR:
    maxR = r
    worst = v

  if r < minR:
    minR = r
    best = v

srt = sorted(cars2, key=lambda t: t[4])
for i in srt:
  print(i)

print(),print(),print()
print(url)
print("Number of cars: ",len(cars2))
print("MAX: ",maxY,maxKm,maxKr)
print("best ",best)
print("worst ",worst)