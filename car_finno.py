# https://www.finn.no/car/used/search.html?dealer_segment=3&engine_fuel=0%2F1&location=20016&price_from=0&price_to=500000&registration_class=1&sort=4

import requests

nrow      = '10000'
priceFrom = '0'
priceTo   = '500000'
# add body_type=4 for stationvagon
url       = 'https://www.finn.no/car/used/search.html?'\
            'dealer_segment=3&engine_fuel=0%2F1&location=20016&'\
            'price_from='+priceFrom+'&price_to='+priceTo+'&'\
            'registration_class=1&sort=4&rows='+nrow

print(url)
response = requests.get(url)

cars = []

s = -1
link  = ''
year  = ''
km    = ''
kr    = ''
maxY  = 0
maxKm = 0
maxKr = 0
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
    elif s==1 and 'ads__unit__content__keys' in line:
      s = 2
    elif s==2:
      tag = '<span>'
      year = int(line[line.find(tag)+len(tag):line.find('</span>')])
      if year > maxY:
        maxY = year
      s = 3
    elif s==3:
      tag = '<span>'
      km = line[line.find(tag)+len(tag):line.find(' km</span>')]
      km = ''.join(km.split())
      km = int(float(km))
      if km > maxKm and km!=12345678 and km!=99999999 and km!=0:
        maxKm = km
      s = 4
    elif s==4:
      tag = '<span>'
      kr = line[line.find(tag)+len(tag):line.find(' kr</span>')]
      kr = ''.join(kr.split())
      kr = int(float(kr))
      if kr > maxKr:
        maxKr = kr      

      if km!=12345678 and km!=99999999 and km!=0:
        cars.append([link, year, km, kr])

      s = -1

minR = 10.0
maxR = -1.0
best = ''
worst = ''
cars2 = []
for i in cars:
  year = i[1]
  km = i[2]
  kr = i[3]

  yi = maxY/year-1
  kmi = km/maxKm
  kri = kr/maxKr
  r = yi + kmi + kri

  v = (i[0],i[1],i[2],i[3],r)
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