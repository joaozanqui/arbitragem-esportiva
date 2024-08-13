def renomear(campeonato_nome, times1, times2):
    campeonatos = {
        'brasileirao': brasileirao,
        'brasileiraob': brasileiraob,
        'brasileiraoc': brasileiraoc,
        'brasileiraod': brasileiraod,
        'copadobrasil': copadobrasil,
        'inglaterra1': inglaterra1,
        'argentina1': argentina1,
        'libertadores': libertadores
    }
    campeonatos.get(campeonato_nome)(times1)
    campeonatos.get(campeonato_nome)(times2)

def brasileirao(times):
    for i in range(len(times)):
        if "Athletico" in times[i] or "Paranaense" in times[i]:
            times[i] = "Athletico Paranaense"
        elif "tico GO" in times[i] or "tico-GO" in times[i] or "Goianiense" in times[i]:
            times[i] = "Atlético Goianiense"
        elif "tico-MG" in times[i] or "tico MG" in times[i] or "Mineiro" in times[i]:
            times[i] = "Atlético Mineiro"
        elif "Bahia" in times[i]:
            times[i] = "Bahia"
        elif "Botafogo" in times[i]:
            times[i] = "Botafogo"
        elif "Bragantino" in times[i]:
            times[i] = "Bragantino"
        elif "Corinthians" in times[i]:
            times[i] = "Corinthians"
        elif "Criciúma" in times[i] or "Criciuma" in times[i]:
            times[i] = "Criciúma"
        elif "Cruzeiro" in times[i]:
            times[i] = "Cruzeiro"
        elif "Cuiabá" in times[i] or "Cuiaba" in times[i]:
            times[i] = "Cuiabá"
        elif "Flamengo" in times[i]:
            times[i] = "Flamengo"
        elif "Fluminense" in times[i]:
            times[i] = "Fluminense"
        elif "Fortaleza" in times[i]:
            times[i] = "Fortaleza"
        elif "Juventude" in times[i]:
            times[i] = "Juventude"
        elif "Grêmio" in times[i] or "Gremio" in times[i]:
            times[i] = "Grêmio"
        elif "Inter" in times[i]:
            times[i] = "Internacional"
        elif "Palmeiras" in times[i]:
            times[i] = "Palmeiras"
        elif "Paulo" in times[i]:
            times[i] = "São Paulo"
        elif "Vasco" in times[i]:
            times[i] = "Vasco da Gama"
        elif "Vitória" in times[i] or "Vitoria" in times[i]:
            times[i] = "Vitória"

def brasileiraob(times):
    for i in range(len(times)):
        if "Amazonas" in times[i]:
            times[i] = "Amazonas"
        elif "rica-MG" in times[i] or "rica MG" in times[i] or "rica FC" in times[i]:
            times[i] = "América Mineiro"
        elif "Avai"  in times[i] or "Avaí" in times[i]:
            times[i] = "Avaí"
        elif "Botafogo" in times[i]:
            times[i] = "Botafogo-SP"
        elif "Brusque" in times[i]:
            times[i] = "Brusque"
        elif "Ceara" in times[i] or "Ceará" in times[i]:
            times[i] = "Ceará"
        elif "Chapecoense" in times[i]:
            times[i] = "Chapecoense"
        elif "Coritiba" in times[i]:
            times[i] = "Coritiba"
        elif "CRB" in times[i] or "CR Brasil" in times[i] or "Clube de Regatas Brasil" in times[i]:
                times[i] = "CRB"
        elif "Goias" in times[i] or "Goiás" in times[i]:
            times[i] = "Goiás"
        elif "Guarani" in times[i] or "Guaraní" in times[i]:
            times[i] = "Guarani"
        elif "Ituano" in times[i]:
            times[i] = "Ituano"
        elif "Mirassol" in times[i]:
            times[i] = "Mirassol"
        elif "Novorizontino" in times[i]:
            times[i] = "Novorizontino"
        elif "Operário" in times[i] or "Operario" in times[i]:
            times[i] = "Operário"
        elif "Paysandu" in times[i]:
            times[i] = "Paysandu"
        elif "Ponte Preta" in times[i]:
            times[i] = "Ponte Preta"
        elif "Santos" in times[i]:
            times[i] = "Santos"
        elif "Sport" in times[i] or "Recife" in times[i]:
            times[i] = "Sport"
        elif "Vila Nova" in times[i]:
            times[i] = "Vila Nova"

def brasileiraoc(times):
    for i in range(len(times)):
        if "ABC" in times[i]:
            times[i] = "ABC"
        if "Aparecidense" in times[i]:
            times[i] = "Aparecidense"
        elif "Athletic Club" in times[i]:
            times[i] = "Athletic Club"
        elif "Botafogo" in times[i]:
            times[i] = "Botafogo-PB"
        elif "Caxias" in times[i]:
            times[i] = "Caxias"
        if "Confiança" in times[i] or "Confianca" in times[i]:
            times[i] = "Confiança"
        elif "CS Alagoano" in times[i] or "CSA" in times[i]:
            times[i] = "CSA"
        elif "Ferroviaria" in times[i] or "Ferroviária" in times[i]:
            times[i] = "Ferroviária"
        elif "Ferroviario" in times[i] or "Ferroviário" in times[i]:
            times[i] = "Ferroviário"
        elif "Figueirense" in times[i]:
            times[i] = "Figueirense"
        elif "Floresta" in times[i]:
            times[i] = "Floresta"
        elif "Londrina" in times[i]:
            times[i] = "Londrina"
        elif "Náutico" in times[i] or "Nautico" in times[i]:
            times[i] = "Náutico"
        if "Remo" in times[i]:
            times[i] = "Remo"
        if "Sampaio Correa" in times[i] or "Sampaio Corrêa" in times[i]:
            times[i] = "Sampaio Corrêa"
        elif "São Bernardo" in times[i] or "Sao Bernardo" in times[i]:
            times[i] = "São Bernardo"
        elif "São José" in times[i] or "Sao Jose" in times[i]:
            times[i] = "São José"
        elif "Tombense" in times[i]:
            times[i] = "Tombense"
        elif "Volta Redonda" in times[i]:
            times[i] = "Volta Redonda"
        elif "Ypiranga" in times[i]:
            times[i] = "Ypiranga"

def brasileiraod(times):
    for i in range(len(times)):
        if "tico Cearense" in times[i] or "tico-CE" in times[i] or "tico CE" in times[i]:
            times[i] = "Atlético Cearense"
        elif "gua Santa" in times[i]:
            times[i] = "Água Santa"
        elif "Águia" in times[i] or "Aguia" in times[i]:
            times[i] = "Águia de Marabá"
        elif "Altos" in times[i]:
            times[i] = "Altos"
        elif "rica" in times[i]:
            times[i] = "América-RN"
        elif "Avenida" in times[i]:
            times[i] = "Avenida"
        elif "Asa" in times[i] or "Arapiraca" in times[i] or "ASA" in times[i] or "Arapiraquense" in times[i]:
            times[i] = "Asa de Arapiraca"
        elif "Anapolis" in times[i] or "Anápolis" in times[i]:
            times[i] = "Anápolis"
        elif "Audax" in times[i]:
            times[i] = "Audax Rio"
        elif "Barra" in times[i]:
            times[i] = "Barra"
        elif "Brasiliense" in times[i]:
            times[i] = "Brasiliense"
        elif "Brasil de Pelotas" in times[i] or "Brasil RS" in times[i] or "Brasil-RS" in times[i] or "Espotivo Brasil" in times[i]:
            times[i] = "Brasil de Pelotas"
        elif "Cameta" in times[i]:
            times[i] = "Cameta"
        elif "Capital" in times[i]:
            times[i] = "Capital"
        elif "Cascavel" in times[i]:
            times[i] = "Cascavel"
        elif "CRA" in times[i] or "Catalano" in times[i]:
            times[i] = "CRAC"
        elif "Esportiva" in times[i] or "CSE" in times[i]:
            times[i] = "CSE"
        elif "Cianorte" in times[i]:
            times[i] = "Cianorte"
        elif "Concordia" in times[i]:
            times[i] = "Concordia"
        elif "Fluminense" in times[i]:
            times[i] = "Fluminense-PI"
        elif "Hercilio Luz" in times[i]:
            times[i] = "Hercilio Luz"
        elif "Humait" in times[i]:
            times[i] = "Humaitá"
        elif "Ipatinga" in times[i]:
            times[i] = "Ipatinga"
        elif "Iguatu" in times[i]:
            times[i] = "Iguatu"
        elif "Ipora" in times[i] or "Iporá" in times[i]:
            times[i] = "Iporá"
        elif "Inter de Limeira" in times[i]:
            times[i] = "Inter de Limeira"
        elif "Itabaiana" in times[i]:
            times[i] = "Itabaiana"
        elif "Itabuna" in times[i]:
            times[i] = "Itabuna"
        elif "Jacuipense" in times[i]:
            times[i] = "Jacuipense"
        elif "Juazeirense" in times[i]:
            times[i] = "Juazeirense"
        elif "Manaus" in times[i]:
            times[i] = "Manaus"
        elif "Manauara" in times[i] or "Manaura" in times[i]:
            times[i] = "Manauara"
        elif "Maring" in times[i]:
            times[i] = "Maringá"
        elif "Maracan" in times[i]:
            times[i] = "Maracanã"
        elif "Maranh" in times[i]:
            times[i] = "Maranhão"
        elif "Mixto" in times[i]:
            times[i] = "Mixto"
        elif "Moto Club" in times[i]:
            times[i] = "Moto Club"
        elif "Nova Iguacu" in times[i] or "Nova Iguaçu" in times[i]:
            times[i] = "Nova Iguaçu"
        elif "Novo Hamburgo" in times[i]:
            times[i] = "Novo Hamburgo"
        elif "Patrocinense" in times[i]:
            times[i] = "Patrocinense"
        elif "Petrolina" in times[i]:
            times[i] = "Petrolina"
        elif "Porto Velho" in times[i]:
            times[i] = "Porto Velho"
        elif "Potiguar" in times[i]:
            times[i] = "Potiguar"
        elif "Portuguesa" in times[i]:
            times[i] = "Portuguesa-RJ"
        elif "Princesa" in times[i]:
            times[i] = "Princesa"
        elif "Real Brasilia" in times[i]:
            times[i] = "Real Brasilia"
        elif "Retr" in times[i]:
            times[i] = "Retrô"
        elif "Rio Branco" in times[i]:
            times[i] = "Rio Branco"
        elif "Uniao EC" in times[i] or "Rondonopolis" in times[i] or "Rondonopolis" in times[i]:
            times[i] = "Rondonópolis"
        elif "Raimundo" in times[i]:
            times[i] = "São Raimundo"
        elif "River" in times[i]:
            times[i] = "River"
        elif "Santa Cruz" in times[i]:
            times[i] = "Santa Cruz-RN"
        elif "Serra" in times[i]:
            times[i] = "Serra"
        elif "Sousa" in times[i]:
            times[i] = "Sousa"
        elif "Sergipe" in times[i]:
            times[i] = "Sergipe"
        elif "Tocantinópolis" in times[i] or "Tocantinopolis" in times[i]:
            times[i] = "Tocantinópolis"
        elif "Trem" in times[i]:
            times[i] = "Trem"
        elif "Treze" in times[i] or "Trese" in times[i]:
            times[i] = "Treze"

def copadobrasil(times):
    for i in range(len(times)):
        if "Athletico" in times[i] or "Paranaense" in times[i]:
            times[i] = "Athletico Paranaense"
        elif "tico GO" in times[i] or "tico-GO" in times[i] or "Goianiense" in times[i]:
            times[i] = "Atlético Goianiense"
        elif "tico-MG" in times[i] or "tico MG" in times[i] or "Mineiro" in times[i]:
            times[i] = "Atlético Mineiro"
        elif "Bahia" in times[i]:
            times[i] = "Bahia"
        elif "Botafogo" in times[i]:
            times[i] = "Botafogo"
        elif "Bragantino" in times[i]:
            times[i] = "Bragantino"
        elif "Corinthians" in times[i]:
            times[i] = "Corinthians"
        elif "CRB" in times[i] or "CR Brasil" in times[i] or "Clube de Regatas Brasil" in times[i]:
                times[i] = "CRB"
        elif "Flamengo" in times[i]:
            times[i] = "Flamengo"
        elif "Fluminense" in times[i]:
            times[i] = "Fluminense"
        elif "Juventude" in times[i]:
            times[i] = "Juventude"
        elif "Grêmio" in times[i] or "Gremio" in times[i]:
            times[i] = "Grêmio"
        elif "Palmeiras" in times[i]:
            times[i] = "Palmeiras"
        elif "Paulo" in times[i]:
            times[i] = "São Paulo"
        elif "Vasco" in times[i]:
            times[i] = "Vasco da Gama"

def inglaterra1(times):
    for i in range(len(times)):
        if "Arsenal" in times[i]:
            times[i] = "Arsenal"
        if "Aston" in times[i]:
            times[i] = "Aston Villa"
        if "Bournemouth" in times[i]:
            times[i] = "Bournemouth"
        if "Brentford" in times[i]:
            times[i] = "Brentford"
        if "Brighton" in times[i]:
            times[i] = "Brighton"
        if "Chelsea" in times[i]:
            times[i] = "Chelsea"
        if "Crystal" in times[i]:
            times[i] = "Crystal Palace"
        if "Everton" in times[i]:
            times[i] = "Everton"
        if "Fulham" in times[i]:
            times[i] = "Fulham"
        if "Ipswich" in times[i]:
            times[i] = "Ipswich Town"
        if "Leicester" in times[i]:
            times[i] = "Leicester"
        if "Liverpool" in times[i]:
            times[i] = "Liverpool"
        if "Man" in times[i] and "City" in times[i]:
            times[i] = "Manchester City"
        if "Man" in times[i] and ("United" in times[i] or "Utd" in times[i]):
            times[i] = "Manchester United"
        if "Newcastle" in times[i]:
            times[i] = "Newcastle"
        if "Nottingham" in times[i] or "Nott" in times[i]:
            times[i] = "Nottingham Forest"
        if "Southampton" in times[i]:
            times[i] = "Southampton"
        if "Tottenham" in times[i] or "Spurs" in times[i]:
            times[i] = "Tottenham"
        if "West" in times[i]:
            times[i] = "West Ham"
        if "Wolve" in times[i]:
            times[i] = "Wolves"

def argentina1(times):
    for i in range(len(times)):
        if "Argentinos" in times[i]:
            times[i] = "Argentinos Juniors"
        elif "Tucuman" in times[i] or "Tucumán" in times[i]:
            times[i] = "Atlético Tucumán"
        elif "Banfield" in times[i]:
            times[i] = "Banfield"
        elif "Barracas" in times[i]:
            times[i] = "Barracas Central"
        elif "Belgrano" in times[i]:
            times[i] = "Belgrano"
        elif "Boca" in times[i]:
            times[i] = "Boca Juniors"
        elif "Central Cordoba" in times[i] or "Central Córdoba" in times[i]:
            times[i] = "Central Córdoba"
        elif "Defensa" in times[i] or "Defesa" in times[i]:
            times[i] = "Defensa y Justicia"
        elif "Riestra" in times[i]:
            times[i] = "Deportivo Riestra"
        elif "Estudiantes" in times[i]:
            times[i] = "Estudiantes de La Plata"
        elif "Gimnasia" in times[i] or "GLP" in times[i]:
            times[i] = "Gimnasia La Plata"
        elif "Godoy" in times[i]:
            times[i] = "Godoy Cruz"
        elif "Huracan" in times[i] or "Huracán" in times[i]:
            times[i] = "Huracán"
        elif "Independiente" in times[i] and "Rivadavia" not in times[i]:
            times[i] = "Independiente"
        elif "Independiente Rivadavia" in times[i] or "RIV" in times[i]:
            times[i] = "Independiente Rivadavia"
        elif "Instituto" in times[i]:
            times[i] = "Instituto Córdoba"
        elif "Lanus" in times[i] or "Lanús" in times[i]:
            times[i] = "Lanús"
        elif "Newell" in times[i]:
            times[i] = "Newell's Old Boys"
        elif "Platense" in times[i]:
            times[i] = "Platense"
        elif "Racing" in times[i]:
            times[i] = "Racing"
        elif "River" in times[i]:
            times[i] = "River Plate"
        elif "Rosario" in times[i] or "Rosário" in times[i]:
            times[i] = "Rosário Central"
        elif "San Lorenzo" in times[i]:
            times[i] = "San Lorenzo"
        elif "Sarmiento" in times[i]:
            times[i] = "Sarmiento"
        elif "Talleres" in times[i]:
            times[i] = "Talleres"
        elif "Tigre" in times[i]:
            times[i] = "Tigre"
        elif "Union" in times[i] or "Unión" in times[i]:
            times[i] = "Unión Santa Fe"
        elif "Velez" in times[i] or "Vélez" in times[i]:
            times[i] = "Vélez Sarsfield"

def libertadores(times):
    for i in range(len(times)):
        if "tico-MG" in times[i] or "tico MG" in times[i] or "Mineiro" in times[i]:
            times[i] = "Atlético Mineiro"
        elif "Bolivar" in times[i]:
            times[i] = "Bolivar"
        elif "Botafogo" in times[i]:
            times[i] = "Botafogo"
        elif "Colo" in times[i]:
            times[i] = "Colo Colo"
        elif "Flamengo" in times[i]:
            times[i] = "Flamengo"
        elif "Fluminense" in times[i]:
            times[i] = "Fluminense"
        elif "Grêmio" in times[i] or "Gremio" in times[i]:
            times[i] = "Grêmio"
        elif "Junior" in times[i] or "Barranquilla" in times[i]:
            times[i] = "Junior Barranquilla"
        elif "Nacional" in times[i]:
            times[i] = "Nacional"
        elif "Palmeiras" in times[i]:
            times[i] = "Palmeiras"
        elif "River" in times[i]:
            times[i] = "River Plate"
        elif "San Lorenzo" in times[i]:
            times[i] = "San Lorenzo"
        elif "Paulo" in times[i]:
            times[i] = "São Paulo"
        elif "Penarol" in times[i] or "Peñarol" in times[i]:
            times[i] = "Peñarol"
        elif "Talleres" in times[i]:
            times[i] = "Talleres"
        elif "Strongest" in times[i]:
            times[i] = "The Strongest"