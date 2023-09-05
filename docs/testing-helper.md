## Testimise Juhised

### Eeltingimused:
- Testimiseks eeldame, et kasutatakse Chrome'i.

### Alustamine:
Enne testimise alustamist veenduge, et olete "Incognito mode" režiimis. Seejärel avage Chrome'i inspekteerimise vahekaart, kasutades klahvikombinatsiooni `CTRL+SHIFT+J`.
Märkus: Inspekteerimisrežiimi aknas soovitame jälgida vahekaarte "Network", "Application" ja "Console".

#### Network
Siin näete päringute liiklust. Liikluse "edukuse" hindamiseks kasutage järgmisi koode:
- Head tulemused:
    - Kood 200 - Päring on jõudnud sihtpunkti ning saanud vastuse.
    - Kood 300 - Päring on suunatud ja jõudnud sihtpunkti.
- Halvad tulemused:
    - Kood 303 - Päring on suunatud, kuid ei jõudnud sihtpunkti.
        Sel juhul on päring "õhus" ja tavaliselt viitab see backendi valele seadistusele, kuigi on erandeid.
    - Koodid 400 ja 404 - Päring ei jõua sihtpunkti, sihtpunkt pole saadaval.
        Sel juhul ei ole päring liikunud frontendist backendi. Põhjused võivad olla mitmekesised, näiteks vale DSL-seadistus või sihtpunkti (konteiner) puudumine.
    - Kood 502 - Lüüsi viga.
        Tavaliselt seotud probleemiga lüüsiga. Backen probleem

#### Application
"Application" vahekaardil kontrollige, et teil pole eelmiste sessioonide küpsiseid alles. Mõnikord ei kustutata neid täielikult isegi pärast Chrome'i täielikku värskendamist. Soovitame igal testimise sammul, kui märkate anomaaliat, kontrollida kõigepealt oma küpsiseid.
Küpsise eemaldamiseks klõpsake vasakut klahvi küpsise nime peal (nt jwt_cookie_name) ja valige rippmenüüst "Kustuta".

#### Console
Konsoolil kuvatakse kõik vead, mida frontend kuvab. Tavaliselt on need seotud ainult frontendiga, kuid harvadel juhtudel võivad olla seotud ka backendiga.
Näiteks, kui frontend otsib oma ressursse (bundle.js jne) vale aadressilt.
Kasutame Reverse Proxy alamradasid vastavalt moodulitele: /analytics, /chat, /training, /services.
Kui otsitavad ressursid ei ole koodis õigesti määratletud, võib tulemus olla tühi leht.

Kui konsoolil kuvatakse veateade, mis umbkaudselt näeb välja: "AXIOS tagastati veakoodiga 300", siis on tegemist vale endpointi suunamisega. Sel juhul on suur tõenäosus, et probleem on backendi seadistuses.
Kui sama viga esineb ka pärast backendi kontrollimist ja näete rida, kus mainitakse ".node_modules/...", siis tuleks probleemi lahendamiseks pöörduda frontendilahenduse poole. Üldiselt on aga probleem tõenäoliselt backendis.

### Dokumenti täiendatakse pidevalt. Kui märkate midagi, mis võiks siin kajastuda, andke sellest teada, ja lisame juurde.
