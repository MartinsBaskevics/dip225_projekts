# Datora komponenšu izdevīguma noteicējs

### Programmas apraksts

Programmas uzdevums ir noteikt potenciālo ietaupījumu vai pārmaksu katrai lietotai datora komponentei sludinājumu portālā `ss.com` balstoties uz `pcpricer.net` datiem.

1. Lietotājam jāizvēlas komponentes veidu (CPU vai GPU), kuru cenas tiks salīdzinātas ar to pašreizējo novecošanās cenu, ja tiek ievadīts kaut kas cits, par to tiek paziņots konsolē un atkārtoti jāievada komponentes veids.
2. Tiek atvērta `ss.com` mājaslapas sadaļa ar konkrētās komponentes sludinājumiem, tiek noteikts to skaits un tiek apskatīts katrs sludinājums.
3. Tiek atrasta komponentes cena un ar regex palīdzību sludinājuma aprakstā tiek atrasts komponentes modelis, tiek izveidots `results.csv` fails ar informāciju par komponentes veidu, modeli, saiti un cenu.
4. Tiek atvērta `pcpricer.net` mājaslapas sadaļa ar konkrētās komponentes meklēšanas tabulu, tajā tiek ierakstīts modelis un izgūta aprēķinātā nolietojuma cena dolāros, kas tiek pārveidota par eiro.
5. Tiek aprēķināts ietaupījums (pozitīvs skaitlis nozīmē cik var ietaupīt, negatīvs skaitlis nozīmē cik var pazaudēt).
6. Tiek atjaunots `results.csv` fails pievienojot tam vēl vienu kolonnu ar ietaupījumu.

Programmas mērķis ir atrast izdevīgus sludinājumus, tā lai sakomplektētu datoru par izdevīgu cenu, vai arī, lai pēcāk pārdotu iegādātās komponentes par to patieso vērtību.

### Ievades dati
Vienīgie ievades dati ir komponentes veids, kas tiek pieprasīts no lietotāja, lai varētu apskatīt konkrētās komponentes veida sludinājumus.

### Izvades dati
Programma izvada `results.csv` failu, kurā saglabājas komponentes veids, modelis, links, cena un ietaupījums. Ja ietaupījums ir pozitīvs, tātad ir izdevīgs pirkums, ja negatīvs, tad nav izdevīgs pirkums. Programma neņem vērā to vai piemēram, procesoram sludinājumā papildus cenā ir iekļauta mātesplate vai dzesētājs, `pcpricer.net` mājaslapā tiek aprēķināta tikai procesora cena.

### Izmantotās bibliotēkas

1. Selenium - atbalsta pārlūkprogrammas automatizāciju.
2. Time - piedāvā dažādas ar laiku saistītas funkcijas.
3. Re - simbolu virkne, kas definē meklējamo izteiksmi.
4. Csv - ievieš klases, lai lasītu un rakstītu datus CSV formātā.

Programmā selenium tiek izmantots, lai piekļūtu `ss.com` mājaslapas datoru komplektēšanas, konkrētās komponentes sadaļai un izgūtu datus par lapu skaitu un sludinājumu skaitu lapā. Ir nepieciešama time bibliotēka, lai radītu sekundes aizkavi atļaujot `ss.com`, kā arī pēcāk `pcpricer.net` ielādēties. Saitē `ss.com` tiek piekļūts katram sludinājumam un ar re bibliotēkas palīdzību tiek aprakstīta simbolu virkne intel un amd procesoriem, kā arī nvidia videokartēm, kuras jāizgūst no sludinājuma apraksta. Ar csv bibliotēku tiek izveidots csv fails, kurā tiek ierakstīta un saglabāta izgūtā informācija no abām saitēm `ss.com` un `pcpricer.net`.

### Video piemērs
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/u2nRiC_fTWU/0.jpg)](https://www.youtube.com/watch?v=u2nRiC_fTWU)
