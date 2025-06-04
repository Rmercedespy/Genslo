import os
import math
import pathlib
import streamlit as st
#from io import BytesIO

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

def obtener(longitudFranja,anchuraFranja,
                bordeInterior,divergencia,disprimerseccion,mprimerseccion,dseg,mseg,secch,
                radio,altura,
                linterior,distextremo,ddivergencia,anchofinal,longitud,pendiente,
                tpendiente,
                pendiente_conica,altura_conica):

    global documentoFinalKml, nombreFinal

    a=longitudFranja
    b=anchuraFranja
    
    ainterior=bordeInterior
    bdivergencia=divergencia
    distprimer=disprimerseccion
    mprim=mprimerseccion
    distsegunda=dseg
    msegunda=mseg
    seccionH=secch

    hi_radio=radio
    hi_altura=altura

    dep_linterior=linterior
    dep_distextremo=distextremo
    dep_divergencia=ddivergencia
    dep_anchofinal=anchofinal
    dep_longitud=longitud
    dep_pendiente=pendiente

    tran_pendiente=tpendiente

    c_pendiente=pendiente_conica
    c_altura=altura_conica

    if float(txt_long1) > 0:
        combo3 = 'N'  
    else:
        combo3 = 'S'
        
    hmf=str(combo3)
    umbral1Long=float(txt_long1)
    umbral1Lat=float(txt_lat1)
    umbral1Elev=float(txt_elev1)
    umbral1total=str(umbral1Long) +','+ str(umbral1Lat)+',' + str(umbral1Elev)
    umbral2Long=float(txt_long2)
    umbral2Lat=float(txt_lat2)
    umbral2Elev=float(txt_elev2)
    umbral2total=str(umbral2Long)+',' + str(umbral2Lat) +','+ str(umbral2Elev)
    ancho_pista=float(txt_anchoPista)
    nombreaerop=txt_aeropuerto+'_'
    nombrepista=txt_pista
    #print(f'{umbral1total} {umbral2total}')

        # ==========================================================
    styloColor1='  <!-- Begin Style Definitions -->\n\
  <Style id="pista"> \n\
    <LineStyle>\n \
      <color>FF0000FF</color>\n\
      <width>1</width>\n\
    </LineStyle>\n\
  </Style>\n\
  <Style id="Franja"> \n\
    <PolyStyle> \n\
      <color>640078B4</color> \n\
    </PolyStyle> \n\
  </Style> \n\
  <Style id="HI"> \n\
    <PolyStyle> \n\
      <color>64F0B414</color> \n\
    </PolyStyle> \n\
  </Style> \n\
  <Style id="C"> \n\
    <PolyStyle> \n\
      <color>64F0E614</color> \n\
    </PolyStyle> \n\
  </Style> \n\
  <Style id="ASC"> \n\
    <PolyStyle> \n\
      <color>647828F0</color> \n\
    </PolyStyle> \n\
  </Style> \n\
  <Style id="Resa"> \n\
    <PolyStyle> \n\
      <color>E6E74C3C</color> \n\
    </PolyStyle> \n\
  </Style> \n\
  <Style id="Aprox"> \n\
    <PolyStyle> \n\
      <color>641400FF</color> \n\
    </PolyStyle> \n\
  </Style> \n\
  <Style id="Aprox2"> \n\
    <PolyStyle> \n\
      <color>641478FF</color> \n\
    </PolyStyle> \n\
  </Style> \n\
  <Style id="Aprox3"> \n\
    <PolyStyle> \n\
      <color>6414F0FF</color> \n\
    </PolyStyle> \n\
  </Style> \n\
  <Style id="TRAN"> \n\
    <PolyStyle> \n\
      <color>64009614</color> \n\
    </PolyStyle> \n\
  </Style> \n\
  <Style id="Pista1"> \n\
    <PolyStyle> \n\
      <color>CB4D5656 </color> \n\
    </PolyStyle> \n\
  </Style> \n' #FF000000: color Negro, se define el color general    



    #***** Conversor de Geograficas a UTM ********
    #*****************************************************
    def convertir_dec_utm(thrLong,thrLat,select_hmf):
        #thrLong
        a=6378137.0 #semieje mayor
        b=6356752.31414#245 #semieje menor
        c=(a**2)/b #radio polar de curvatura
        thr_Long=(math.radians(float(thrLong)))
        thr_Lat=math.radians(float(thrLat))
        exc=(math.sqrt(a**2-b**2))/a #excentricidad
        ei=(math.sqrt(a**2-b**2))/b #segunda excentricidad
        Ni=(c/(math.sqrt(1+(ei**2)*(math.cos(thr_Lat))**2)))*0.9996##**
        Huso=math.trunc((thrLong/6)+31) #math.trunc obtiene la parte entera del numero
        merid_uso=(6*Huso)-183# meridiano central
        deltalambda=(thr_Long)-(merid_uso*math.pi/180) # distancia angular entre el punto y el meridiano central dl huso (rad)
        A=math.cos(thr_Lat)*math.sin(deltalambda)##**
        Xi=(1/2)*math.log((1+A)/(1-A)) ##+++++
        Z=((ei**2)/2)*Xi**2*(math.cos(thr_Lat))**2##**
        xEste=(Xi*Ni*(1+(Z/3)))+500000
               
        # ****Calculo del Norte********
        A1=math.sin(2*thr_Lat)#**
        J2=thr_Lat+(A1/2)#**
        A2=A1*(math.cos(thr_Lat))**2#**
        J4=(3*J2+A2)/4#**
        J6=(5*J4+A2*(math.cos(thr_Lat))**2)/3#**
        alfa=(3/4)*ei**2 # Aplanamiento
        Gama=(35/27)*alfa**3#**
        Beta=(5/3)*alfa**2#**
        Bfi=0.9996*c*(thr_Lat-alfa*J2+Beta*J4-Gama*J6)#**
        Eta=(math.atan((math.tan(thr_Lat))/(math.cos(deltalambda))))-(thr_Lat)##**
        yN=Eta*Ni*(1+Z)+Bfi
        #seleccionar Hemisferio
        if select_hmf=='S':
            yNorte=yN+10000000
        elif select_hmf=='N':
            yNorte=yN
        return xEste,yNorte,Huso

    #************ Conversor de  UTM a Geograficas ********
    #*****************************************************
    def convertir_utm_dec(UTM_Long,UTM_Lat,select_hmf,huso):
        a=6378137.0 #semieje mayor
        b=6356752.31414 #semieje menor
        c=6399593.62586#(a**2)/b #radio polar de curvatura
        lambdaO=(huso*6)-183
        ei=0.082094438153
        cord_Long=float(UTM_Long)-500000 # cordenada X -- ABSCISA
        # CONDICIONAL PARA VERIFICAR SI ES SUR O NORTE
        if select_hmf=='S':
            cord_Lat=float(UTM_Lat)-10000000
        elif select_hmf=='N':
            cord_Lat=float(UTM_Lat)
        fi=cord_Lat/(6366197.724*0.9996)
        v=(c/(math.sqrt(1+((ei**2)*(math.cos(fi))**2))))*0.9996
        ai=cord_Long/v
        A1=math.sin(2*fi)
        A2=A1*(math.cos(fi))**2
        J2=fi+(A1/2)
        J4=(3*J2+A2)/4
        J6=(5*J4+A2*(math.cos(fi)**2))/3
        alfa=(3/4)*ei**2
        beta=(5/3)*alfa**2
        gama=(35/27)*alfa**3
        Bo=0.9996*c*(fi-alfa*J2+beta*J4-gama*J6)
        bi=(cord_Lat-Bo)/v
        zet=((ei**2*ai**2)/2)*(math.cos(fi))**2
        eta=ai*(1-(zet/3))
        ni=bi*(1-zet)+fi
        sinE=(((math.e)**eta)-((math.e)**(-1*eta)))/2
        deltaLambda=math.atan(sinE/math.cos(ni))
        taoi=math.atan(math.cos(deltaLambda)*math.tan(ni))
        Longitud_GEO=(deltaLambda*180/math.pi)+lambdaO #este es el valor de la Longitud
        Latitud_GEO1=fi+(1+(ei)**2*math.cos(fi)**2-(3/2)*ei**2*math.sin(fi)*math.cos(fi)*(taoi-fi))*(taoi-fi)
        Latitud_GEO=Latitud_GEO1*180/math.pi
        Longitud_GEO = round(Longitud_GEO, 5)
        Latitud_GEO = round(Latitud_GEO, 5)
        return Longitud_GEO,Latitud_GEO

   
##    print(f' {a} {b}' )

    # ******** PISTA ************
    P1Long,P1Lat,huso=convertir_dec_utm(umbral1Long,umbral1Lat,hmf)
##    print(f'P1Long :{P1Long}  \n  P1Lat: {P1Lat}')
    P2Long,P2Lat,huso=convertir_dec_utm(umbral2Long,umbral2Lat,hmf)
    #print(f'P2Long :{P2Long}    P2Lat: {P2Lat}')
    # Funcion de distancia: con las cordenadas en UTM
    def distancia(pln1,plt1,pln2,plt2):
        dist=math.sqrt(((pln1-pln2)**2)+((plt1-plt2)**2))
        return dist

    distance=distancia(P1Long,P1Lat,P2Long,P2Lat)
    #print(f" distancia entre umbrales es: {distance} metros")

    #Calculo de Azimut: angulo medido en sentido horario desde la vertical (Norte geografico)
    if P1Long>P2Long:
        mpendiente=(P2Lat-P1Lat)/(P2Long-P1Long)
        if mpendiente<0:

            alfaaz=math.asin(abs(P2Long-P1Long)/distance)
            alfasexag=alfaaz*180/math.pi
            azimut=180-alfasexag
            alfaprima=abs(azimut-90)
        elif mpendiente>0:

            betaaz=math.acos(abs(P2Long-P1Long)/distance)#  se obtiene en radianes
            alfaaz=betaaz+(math.pi/2) #suma de beta + 90
            alfasexag=alfaaz*180/math.pi#sexagesimales
            azimut=180-alfasexag
            alfaprima=(azimut-90)
    elif P1Long<P2Long:
        mpendiente=(P1Lat-P2Lat)/(P1Long-P2Long)
        if mpendiente<0:

            alfaaz=math.asin(abs(P2Long-P1Long)/distance)
##            print(f' alfaaz: {alfaaz}')
            alfasexag=alfaaz*180/math.pi
            azimut=180-alfasexag
            alfaprima=abs(azimut-90)
           
        elif mpendiente>0:

            betaaz=math.acos(abs(P2Long-P1Long)/distance)#  devuelve en radianes
            alfaaz=betaaz+(math.pi/2) #suma de beta + 90
            alfasexag=alfaaz*180/math.pi#sexagesimales
            azimut=180-alfasexag
            alfaprima=(azimut-90)
   
    #print(f" El azimut es : {azimut}")
   
    #print(f" Alfaprima: {alfaprima}")
    #print(f" alfaprimas=(azimut-90): {alfaprimas}")

    semiancho_pista=ancho_pista/2
    # ******************************************************************************************
    #**** Calculo de las cordenadas de vertices de EJE DE PISTA EN UTM por ambos lados***********
    # ******************************************************************************************

    def vertices(angulosig,longitud,latitud,lado):
        if lado=='d':
##            print(longitud)
            angul=math.sin(math.radians(angulosig))
##            print(f" math.sin(angulosig): {angul}")
            vertice_Long=longitud+semiancho_pista*math.sin(math.radians(angulosig))# el abs nos asegura que el sen sea siempre positivo
##            print(latitud)
            vertice_Lat=latitud+semiancho_pista*(math.cos(math.radians(angulosig)))
        elif lado=='i':
            vertice_Long=longitud-semiancho_pista*math.sin(math.radians(angulosig)) # el abs nos asegura que el sen sea siempre positivo
            vertice_Lat=latitud-semiancho_pista*(math.cos(math.radians(angulosig)))
        return vertice_Long,vertice_Lat
    def verticesfranja(angulosig,longitud,latitud,lado,b_ancho):
        if lado=='d':
          #  print(longitud)
            #angul=math.sin(math.radians(angulosig))
           # print(f" math.sin(angulosig): {angul}")
            vertice_Long=longitud+b_ancho*math.sin(math.radians(angulosig))#
            #print(latitud)
            vertice_Lat=latitud+b_ancho*(math.cos(math.radians(angulosig)))# la letra b:  es el ancho de franja llamada desde la variable global
        elif lado=='i':
            vertice_Long=longitud-b_ancho*math.sin(math.radians(angulosig)) #
            vertice_Lat=latitud-b_ancho*(math.cos(math.radians(angulosig)))
        return vertice_Long,vertice_Lat

    # ******************************************************************************************
    #**** Calculo de las cordenadas de vertices para cualquier lado ****************************
    # ******************************************************************************************
   
    def verticesLibre1(longitud,latitud,dist_to_franja):
        if P1Long<P2Long:
            asd=math.sin(alfaaz)
            distt=dist_to_franja*math.sin(alfaaz)
            asdc=math.cos(alfaaz)
            disttc=dist_to_franja*math.cos(alfaaz)
##            print(f' sin(alfaaz): {asd} dist*sin= {distt}' )
##            print(f' cos(alfaaz): {asdc} dist*cos= {disttc}')
            vertice_Long1=longitud-dist_to_franja*math.sin(alfaaz)
            vertice_Lat1=latitud+dist_to_franja*(math.cos(alfaaz))

        elif P1Long>P2Long:
            vertice_Long1=longitud+dist_to_franja*math.sin(alfaaz)
            vertice_Lat1=latitud-dist_to_franja*(math.cos(alfaaz))
        #print(f' verticeLong1: {vertice_Long1} \n vertice_Lat1 {vertice_Lat1}')
        return vertice_Long1,vertice_Lat1

    #-----------------------------------------

    def verticesLibre2(longitud,latitud,dist_to_franja):
        if P1Long<P2Long:
            vertice_Long2=longitud+dist_to_franja* math.sin((alfaaz))
            vertice_Lat2=latitud-dist_to_franja*(math.cos((alfaaz)))
        if P1Long>P2Long:
            vertice_Long2=longitud-dist_to_franja*math.sin((alfaaz))
            vertice_Lat2=latitud+dist_to_franja*(math.cos((alfaaz)))
##        print(f' verticeLong2: {vertice_Long2} \n vertice_Lat2 {vertice_Lat2}')
        return vertice_Long2,vertice_Lat2

    #EjecuciOn de funcion para generar vertice a la derecha del eje de pista
    verticederLong1,verticederLat1=vertices(alfaprima,P1Long,P1Lat,'d')
    verticederLong2,verticederLat2=vertices(alfaprima,P2Long,P2Lat,'d')#tambien lleva el alfaprima por ser paralela al eje de pista
    verticederLong3,verticederLat3=vertices(alfaprima,P1Long,P1Lat,'i')
    verticederLong4,verticederLat4=vertices(alfaprima,P2Long,P2Lat,'i')

    #== Ejecucion de funcion para convertir de UTM a DEcimales para cargar en KML
    verticeDecToKMLLong1,verticeDecToKMLLat1=convertir_utm_dec(verticederLong1,verticederLat1,hmf,huso)
    verticeDecToKMLLong2,verticeDecToKMLLat2=convertir_utm_dec(verticederLong2,verticederLat2,hmf,huso)
    verticeDecToKMLLong3,verticeDecToKMLLat3=convertir_utm_dec(verticederLong3,verticederLat3,hmf,huso)
    verticeDecToKMLLong4,verticeDecToKMLLat4=convertir_utm_dec(verticederLong4,verticederLat4,hmf,huso)

     #Eje de Pista

    ejePista='    <Placemark> \n\
      <description>EJE de PISTA</description> \n\
      <styleUrl>#line1</styleUrl> \n\
      <LineString> \n\
        <altitudeMode>absolute</altitudeMode> \n\
        <extrude>0</extrude> \n\
        <coordinates> \n          '+ umbral1total \
        +'\n          ' + umbral2total +'\n        </coordinates>\n\
      </LineString>\n\
    </Placemark>'
    
    #=========== Borde de pista ==============
       # derecha
    vertice1Coord=str(verticeDecToKMLLong1)+','+ str(verticeDecToKMLLat1)+','+ str(umbral1Elev)
    vertice2Coord=str(verticeDecToKMLLong2)+','+ str(verticeDecToKMLLat2)+','+ str(umbral2Elev)
    bordePistaD='    <Placemark> \n\
      <description>RWYLD</description> \n\
      <styleUrl>#line1</styleUrl> \n\
      <LineString> \n\
        <altitudeMode>absolute</altitudeMode> \n\
        <extrude>0</extrude> \n\
        <coordinates> \n          '+ vertice1Coord\
                +'\n          ' + vertice2Coord +'\n        </coordinates>\n\
      </LineString>\n\
    </Placemark>'

       # Izquierda
    vertice3Coord=str(verticeDecToKMLLong3)+','+ str(verticeDecToKMLLat3)+','+ str(umbral1Elev)
    vertice4Coord=str(verticeDecToKMLLong4)+','+ str(verticeDecToKMLLat4)+','+ str(umbral2Elev)
    bordePistaI='    <Placemark> \n\
      <description>RWYLD</description> \n\
      <styleUrl>#line1</styleUrl> \n\
      <LineString> \n\
        <altitudeMode>absolute</altitudeMode> \n\
        <extrude>0</extrude> \n\
        <coordinates> \n          '+ vertice3Coord\
                +'\n          ' + vertice4Coord +'\n        </coordinates>\n\
      </LineString>\n\
    </Placemark>'
       
    # Area de pista
    areaPista='    <Placemark>\n\
      <description>0</description>\n\
      <styleUrl>#Pista1</styleUrl>\n\
      <Polygon>\n\
        <altitudeMode>absolute</altitudeMode>\n\
        <extrude>0</extrude>\n\
        <outerBoundaryIs>\n\
          <LinearRing>\n\
            <coordinates>\n              '+vertice1Coord\
                +'\n              '+vertice2Coord\
                +'\n              '+vertice4Coord\
                +'\n              '+vertice3Coord\
                +'\n              '+vertice1Coord\
                +'\n            </coordinates>\n\
          </LinearRing>\n\
        </outerBoundaryIs>\n\
      </Polygon>\n\
    </Placemark>'
    #**************************************************************************
    # ********************************* FRANJA DE  PISTA **********************
    #**************************************************************************

    verticeProlongacionPistaLong1,verticeProlongacionPistaLat1=verticesLibre1(P1Long,P1Lat,a) #puntos centrales 1
    verticeProlongacionPistaLong2,verticeProlongacionPistaLat2=verticesLibre2(P2Long,P2Lat,a) #puntos centrales 2
    # ---------------- Vertices d franja --------------
    vfranjaderLong1,vfranjaderLat1=verticesfranja(alfaprima,verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,'d',b)
    vfranjaderLong2,vfranjaderLat2=verticesfranja(alfaprima,verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,'d',b)#tambien lleva el alfaprima por ser paralela al eje de pista
    vfranjaderLong3,vfranjaderLat3=verticesfranja(alfaprima,verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,'i',b)
    vfranjaderLong4,vfranjaderLat4=verticesfranja(alfaprima,verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,'i',b)

    #== Ejecucion de funcion para convertir de UTM a DEcimales para cargar en KML *** FRANJA ***
    vfranjaDecToKMLLong1,vfranjaDecToKMLLat1=convertir_utm_dec(vfranjaderLong1,vfranjaderLat1,hmf,huso)
    vfranjaDecToKMLLong2,vfranjaDecToKMLLat2=convertir_utm_dec(vfranjaderLong2,vfranjaderLat2,hmf,huso)
    vfranjaDecToKMLLong3,vfranjaDecToKMLLat3=convertir_utm_dec(vfranjaderLong3,vfranjaderLat3,hmf,huso)
    vfranjaDecToKMLLong4,vfranjaDecToKMLLat4=convertir_utm_dec(vfranjaderLong4,vfranjaderLat4,hmf,huso)
   
    # Franja de Pista ----Cordenadas y areas de FRANJA
    # derecha
    vfranja1Coord=str(vfranjaDecToKMLLong1)+','+ str(vfranjaDecToKMLLat1)+','+ str(umbral1Elev)
    vfranja2Coord=str(vfranjaDecToKMLLong2)+','+ str(vfranjaDecToKMLLat2)+','+ str(umbral2Elev)
    bordeFranjaPistaD='    <Placemark> \n\
      <description>RWYLD</description> \n\
      <styleUrl>#line1</styleUrl> \n\
      <LineString> \n\
        <altitudeMode>absolute</altitudeMode> \n\
        <extrude>0</extrude> \n\
        <coordinates> \n          '+ vfranja1Coord\
                +'\n          ' + vfranja2Coord +'\n        </coordinates>\n\
      </LineString>\n\
    </Placemark>'

       # Izquierda
    vfranja3Coord=str(vfranjaDecToKMLLong3)+','+ str(vfranjaDecToKMLLat3)+','+ str(umbral1Elev)
    vfranja4Coord=str(vfranjaDecToKMLLong4)+','+ str(vfranjaDecToKMLLat4)+','+ str(umbral2Elev)
    bordeFranjaPistaI='    <Placemark> \n\
      <description>RWYLD</description> \n\
      <styleUrl>#line1</styleUrl> \n\
      <LineString> \n\
        <altitudeMode>absolute</altitudeMode> \n\
        <extrude>0</extrude> \n\
        <coordinates> \n          '+ vfranja3Coord\
                +'\n          ' + vfranja4Coord +'\n        </coordinates>\n\
      </LineString>\n\
    </Placemark>'
       
    # Area de FRANJA  pista
    areaFranja='    <Placemark>\n\
      <description>0</description>\n\
      <styleUrl>#Franja</styleUrl>\n\
      <Polygon>\n\
        <altitudeMode>absolute</altitudeMode>\n\
        <extrude>0</extrude>\n\
        <outerBoundaryIs>\n\
          <LinearRing>\n\
            <coordinates>\n              '+vfranja1Coord\
                +'\n              '+vfranja2Coord\
                +'\n              '+vfranja4Coord\
                +'\n              '+vfranja3Coord\
                +'\n              '+vfranja1Coord\
                +'\n            </coordinates>\n\
          </LinearRing>\n\
        </outerBoundaryIs>\n\
        <innerBoundaryIs>\n\
          <LinearRing>\n\
            <coordinates>\n            '+ vertice1Coord\
                +'\n            '+vertice2Coord\
                +'\n            '+vertice4Coord\
                +'\n            '+vertice3Coord\
                +'\n            '+vertice1Coord\
                +'\n          </coordinates>\n\
          </LinearRing>\n\
        </innerBoundaryIs>\n\
      </Polygon>\n\
    </Placemark>'
    #*******************************************************************************************
    #*****************************FIN  DE FRANJA DE PISTA **************************************
    #*******************************************************************************************
   
    #=============================================================================================================
    #=============================================================================================================

    #**************************************************************************
    # *************************************** RESA ****************************
    #**************************************************************************

   
    # ---------------- Vertices de RESA sobre borde de FRANJA--------------
    vresaderLong1,vresaderLat1=verticesfranja(alfaprima,verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,'d',ancho_pista)
    vresaderLong2,vresaderLat2=verticesfranja(alfaprima,verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,'d',ancho_pista)#tambien lleva el alfaprima por ser paralela al eje de pista
    vresaderLong3,vresaderLat3=verticesfranja(alfaprima,verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,'i',ancho_pista)
    vresaderLong4,vresaderLat4=verticesfranja(alfaprima,verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,'i',ancho_pista)
    # ----- Vertices de RESA  complemntarios --------
                    # Puntos centrales
    verticeProlongacion2PistaLong1,verticeProlongacion2PistaLat1=verticesLibre1(verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,90) #puntos centrales 1
    verticeProlongacion2PistaLong2,verticeProlongacion2PistaLat2=verticesLibre2(verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,90) #puntos centrales 2
                   # PUntos complementarios
    vresaderLong5,vresaderLat5=verticesfranja(alfaprima,verticeProlongacion2PistaLong1,verticeProlongacion2PistaLat1,'d',ancho_pista)
    vresaderLong6,vresaderLat6=verticesfranja(alfaprima,verticeProlongacion2PistaLong2,verticeProlongacion2PistaLat2,'d',ancho_pista)#tambien lleva el alfaprima por ser paralela al eje de pista
    vresaderLong7,vresaderLat7=verticesfranja(alfaprima,verticeProlongacion2PistaLong2,verticeProlongacion2PistaLat2,'i',ancho_pista)
    vresaderLong8,vresaderLat8=verticesfranja(alfaprima,verticeProlongacion2PistaLong1,verticeProlongacion2PistaLat1,'i',ancho_pista)

    #== Ejecucion de funcion para convertir de UTM a DEcimales para cargar en KML *** RESA ***
    vresaDecToKMLLong1,vresaDecToKMLLat1=convertir_utm_dec(vresaderLong1,vresaderLat1,hmf,huso)
    vresaDecToKMLLong2,vresaDecToKMLLat2=convertir_utm_dec(vresaderLong2,vresaderLat2,hmf,huso)
    vresaDecToKMLLong3,vresaDecToKMLLat3=convertir_utm_dec(vresaderLong3,vresaderLat3,hmf,huso)
    vresaDecToKMLLong4,vresaDecToKMLLat4=convertir_utm_dec(vresaderLong4,vresaderLat4,hmf,huso)
    vresaDecToKMLLong5,vresaDecToKMLLat5=convertir_utm_dec(vresaderLong5,vresaderLat5,hmf,huso)
    vresaDecToKMLLong6,vresaDecToKMLLat6=convertir_utm_dec(vresaderLong6,vresaderLat6,hmf,huso)
    vresaDecToKMLLong7,vresaDecToKMLLat7=convertir_utm_dec(vresaderLong7,vresaderLat7,hmf,huso)
    vresaDecToKMLLong8,vresaDecToKMLLat8=convertir_utm_dec(vresaderLong8,vresaderLat8,hmf,huso)
   
    # Resa de Pista ----Cordenadas y areas de RESA
    # derecha
    vresa1Coord=str(vresaDecToKMLLong1)+','+ str(vresaDecToKMLLat1)+','+ str(umbral1Elev)
    vresa2Coord=str(vresaDecToKMLLong2)+','+ str(vresaDecToKMLLat2)+','+ str(umbral2Elev)
    vresa5Coord=str(vresaDecToKMLLong5)+','+ str(vresaDecToKMLLat5)+','+ str(umbral1Elev)
    vresa6Coord=str(vresaDecToKMLLong6)+','+ str(vresaDecToKMLLat6)+','+ str(umbral2Elev)
    bordeResaPista1D='    <Placemark> \n\
      <description>RWYLD</description> \n\
      <styleUrl>#line1</styleUrl> \n\
      <LineString> \n\
        <altitudeMode>absolute</altitudeMode> \n\
        <extrude>0</extrude> \n\
        <coordinates> \n          '+ vresa1Coord\
                +'\n          ' + vresa5Coord +'\n\
        </coordinates>\n\
      </LineString>\n\
    </Placemark>'
    bordeResaPista2D='    <Placemark> \n\
      <description>RWYLD</description> \n\
      <styleUrl>#line1</styleUrl> \n\
      <LineString> \n\
        <altitudeMode>absolute</altitudeMode> \n\
        <extrude>0</extrude> \n\
        <coordinates> \n          '+ vresa2Coord\
                +'\n          ' + vresa6Coord +'\n\
        </coordinates>\n\
      </LineString>\n\
    </Placemark>'

       # Izquierda
    vresa3Coord=str(vresaDecToKMLLong3)+','+ str(vresaDecToKMLLat3)+','+ str(umbral2Elev)
    vresa4Coord=str(vresaDecToKMLLong4)+','+ str(vresaDecToKMLLat4)+','+ str(umbral1Elev)
    vresa7Coord=str(vresaDecToKMLLong7)+','+ str(vresaDecToKMLLat7)+','+ str(umbral2Elev)
    vresa8Coord=str(vresaDecToKMLLong8)+','+ str(vresaDecToKMLLat8)+','+ str(umbral1Elev)

    bordeResaPista1I='    <Placemark> \n\
      <description>RWYLD</description> \n\
      <styleUrl>#line1</styleUrl> \n\
      <LineString> \n\
        <altitudeMode>absolute</altitudeMode> \n\
        <extrude>0</extrude> \n\
        <coordinates> \n          '+ vresa4Coord\
                +'\n          ' + vresa8Coord +'\n        </coordinates>\n\
      </LineString>\n\
    </Placemark>'
    bordeResaPista2I='    <Placemark> \n\
      <description>RWYLD</description> \n\
      <styleUrl>#line1</styleUrl> \n\
      <LineString> \n\
        <altitudeMode>absolute</altitudeMode> \n\
        <extrude>0</extrude> \n\
        <coordinates> \n          '+ vresa3Coord\
                +'\n          ' + vresa7Coord +'\n        </coordinates>\n\
      </LineString>\n\
        </Placemark>'
       
    # Area de RESA de  pista
    areaResa1='<Placemark>\n\
          <description>0</description>\n\
          <styleUrl>#Resa</styleUrl>\n\
          <Polygon>\n\
            <altitudeMode>absolute</altitudeMode>\n\
            <extrude>0</extrude>\n\
            <outerBoundaryIs>\n\
              <LinearRing>\n\
                <coordinates>\n'+vresa5Coord\
                +'\n'+vresa1Coord\
                +'\n'+vresa4Coord\
                +'\n'+vresa8Coord\
                +'\n'+vresa5Coord\
                +'\n </coordinates>\n\
              </LinearRing>\n\
                </outerBoundaryIs>\n\
                </Polygon>\n\
        </Placemark>'
    areaResa2='<Placemark>\n\
          <description>0</description>\n\
          <styleUrl>#Resa</styleUrl>\n\
          <Polygon>\n\
            <altitudeMode>absolute</altitudeMode>\n\
            <extrude>0</extrude>\n\
            <outerBoundaryIs>\n\
              <LinearRing>\n\
                <coordinates>\n'+vresa2Coord\
                +'\n'+vresa6Coord\
                +'\n'+vresa7Coord\
                +'\n'+vresa3Coord\
                +'\n'+vresa2Coord\
                +'\n </coordinates>\n\
              </LinearRing>\n\
                </outerBoundaryIs>\n\
                </Polygon>\n\
        </Placemark>'
    #*******************************************************************************************
    #*********************************** FIN  DE RESA ******************************************
    #*******************************************************************************************
    #=============================================================================================================
    #=============================================================================================================

    #********************************************************************************************************
    # ******************************************************* SLO *******************************************
    #********************************************************************************************************

    #*******************************************************************************************
    #----------------------------------- APROXIMACION ------------------------------------------
    #-------------------------------------------------------------------------------------------

    #verticeProlongacionPistaLong1,verticeProlongacionPistaLat1=verticesLibre1(P1Long,P1Lat,a) #punto central sobre la franja donde inicia la sup aproximacion

    #  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!PRIMER SECCION !!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!
    semiainterior=ainterior/2
##    print(f'semiainterior: {semiainterior}')
    #bdivergencia
    #distprimer
    # ---------------- Vertices de APROXIMACION sobre borde de franja--------------Pto 1 y Pto 2
##    print(f'verticeProlongacionPistaLong1: {verticeProlongacionPistaLong1} \n verticeProlongacionPistaLat1: {verticeProlongacionPistaLat1}')
    vaproxinterLong1,vaproxinterLat1=verticesfranja(alfaprima,verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,'d',semiainterior)
    vaproxinterLong2,vaproxinterLat2=verticesfranja(alfaprima,verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,'i',semiainterior)
##    print(f' vaproxinterLong1: {vaproxinterLong1} \n vaproxinterLat1: {vaproxinterLat1}')
##    print(f' vaproxinterLong2: {vaproxinterLong2} \n vaproxinterLat2: {vaproxinterLat2}')
    # ----- Vertices de Aproximacion  complemntarios --------
   
                    # Punto central del final de la PRIMERA SECCION
    verticefinprimersecLong1,verticefinprimersecLat1=verticesLibre1(verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,distprimer) #puntos centrales del fin de primer seccion 1
##    print(f' verticefinprimersecLong1: {verticefinprimersecLong1} \n verticefinprimersecLat1: {verticefinprimersecLat1}')
   
                   # Puntos laterales del fin de la PRIMERA SECCION
    semiainteriorfinalprimer=semiainterior+(distprimer*bdivergencia/100)
    vaproxinterLong3,vaproxinterLat3=verticesfranja(alfaprima,verticefinprimersecLong1,verticefinprimersecLat1,'d',semiainteriorfinalprimer)
##    print(f' vaproxinterLong3 {vaproxinterLong3} \n vaproxinterLat3 {vaproxinterLat3}')
    vaproxinterLong4,vaproxinterLat4=verticesfranja(alfaprima,verticefinprimersecLong1,verticefinprimersecLat1,'i',semiainteriorfinalprimer)
##    print(f' vaproxinterLong4 {vaproxinterLong4} \n vaproxinterLat4 {vaproxinterLat4}')

    #== Ejecucion de funcion para convertir de UTM a DEcimales para cargar en KML *** APROXIMACION *** PRIMERA FUNCION***
    vaproxDecToKMLLong1,vaproxDecToKMLLat1=convertir_utm_dec(vaproxinterLong1,vaproxinterLat1,hmf,huso)
    vaproxDecToKMLLong2,vaproxDecToKMLLat2=convertir_utm_dec(vaproxinterLong2,vaproxinterLat2,hmf,huso)
    vaproxDecToKMLLong3,vaproxDecToKMLLat3=convertir_utm_dec(vaproxinterLong3,vaproxinterLat3,hmf,huso)
    vaproxDecToKMLLong4,vaproxDecToKMLLat4=convertir_utm_dec(vaproxinterLong4,vaproxinterLat4,hmf,huso)
 
   

    # Area de APROXIMACION  ---- Cordenadas y areas de APROXIMACION PRIMER SECCION
    # derecha
    umbralfinprimerseccion=umbral1Elev+(mprim*distprimer/100)
    vaprox1Coord=str(vaproxDecToKMLLong1)+','+ str(vaproxDecToKMLLat1)+','+ str(umbral1Elev)
    vaprox3Coord=str(vaproxDecToKMLLong3)+','+ str(vaproxDecToKMLLat3)+','+ str(umbralfinprimerseccion)
   

 
    bordeAproxPista1D='<Placemark> \n\
                <description>RWYLD</description> \n\
                <styleUrl>#line1</styleUrl> \n\
                <LineString> \n\
                <altitudeMode>absolute</altitudeMode> \n\
                <extrude>1</extrude> \n\
                <coordinates> \n'+ vaprox1Coord\
                +'\n' + vaprox3Coord +'\n\
                </coordinates>\n\
                </LineString>\n\
                </Placemark>'

   

       # Izquierda
    vaprox2Coord=str(vaproxDecToKMLLong2)+','+ str(vaproxDecToKMLLat2)+','+ str(umbral1Elev)
    vaprox4Coord=str(vaproxDecToKMLLong4)+','+ str(vaproxDecToKMLLat4)+','+ str(umbralfinprimerseccion)
 
    bordeAproxPista1I='<Placemark> \n\
                <description>RWYLD</description> \n\
                <styleUrl>#line1</styleUrl> \n\
                <LineString> \n\
                <altitudeMode>absolute</altitudeMode> \n\
                <extrude>0</extrude> \n\
                <coordinates> \n'+ vaprox2Coord\
                +'\n' + vaprox4Coord +'\n\
                </coordinates>\n\
                </LineString>\n\
                </Placemark>'
       
    # Area de Aproximacion de  pista
    areaAprox1='<Placemark>\n\
          <description>0</description>\n\
          <styleUrl>#Aprox</styleUrl>\n\
          <Polygon>\n\
            <altitudeMode>absolute</altitudeMode>\n\
            <extrude>0</extrude>\n\
            <outerBoundaryIs>\n\
                <LinearRing>\n\
                <coordinates>\n'+vaprox1Coord\
                +'\n'+vaprox2Coord\
                +'\n'+vaprox4Coord\
                +'\n'+vaprox3Coord\
                +'\n'+vaprox1Coord\
                +'\n </coordinates>\n\
              </LinearRing>\n\
              </outerBoundaryIs>\n\
            </Polygon>\n\
        </Placemark>'

    #  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!SEGUNDA SECCION !!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!
    # Para la 2da seccion se utiliza el punto final central de la primera seccion para obtener el PUNTO FINAL CENTRAL DE LA SEGUNDA SECCION
    if msegunda=='nd' and distsegunda=='nd':
        pass
    else:
        verticefinSEGUNDAsecLong1,verticefinSEGUNDAsecLat1=verticesLibre1(verticefinprimersecLong1,verticefinprimersecLat1,distsegunda)
        # Vertices laterales del fin de la SEGUNDA SECCION
        semiainteriorfinalsegunda=semiainteriorfinalprimer+(distsegunda*bdivergencia/100)
       
        vaproxinterLong5,vaproxinterLat5=verticesfranja(alfaprima,verticefinSEGUNDAsecLong1,verticefinSEGUNDAsecLat1,'d',semiainteriorfinalsegunda)
        vaproxinterLong6,vaproxinterLat6=verticesfranja(alfaprima,verticefinSEGUNDAsecLong1,verticefinSEGUNDAsecLat1,'i',semiainteriorfinalsegunda)
        #== Ejecucion de funcion para convertir de UTM a DEcimales para cargar en KML *** APROXIMACION *** PRIMERA FUNCION***
        vaproxDecToKMLLong5,vaproxDecToKMLLat5=convertir_utm_dec(vaproxinterLong5,vaproxinterLat5,hmf,huso)
        vaproxDecToKMLLong6,vaproxDecToKMLLat6=convertir_utm_dec(vaproxinterLong6,vaproxinterLat6,hmf,huso)
   
        umbralfinSEGUNDAseccion=umbralfinprimerseccion+(msegunda*distsegunda/100)
        #DERECHA
        vaprox5Coord=str(vaproxDecToKMLLong5)+','+ str(vaproxDecToKMLLat5)+','+ str(umbralfinSEGUNDAseccion)
        #IZQUIERDA
        vaprox6Coord=str(vaproxDecToKMLLong6)+','+ str(vaproxDecToKMLLat6)+','+ str(umbralfinSEGUNDAseccion)

        # Area de APROXIMACION  ---- Cordenadas y areas de APROXIMACION SEGUNDA SECCION
 
        bordeAproxPista2D='<Placemark> \n\
                    <description>RWYLD</description> \n\
                    <styleUrl>#line1</styleUrl> \n\
                    <LineString> \n\
                    <altitudeMode>absolute</altitudeMode> \n\
                    <extrude>1</extrude> \n\
                    <coordinates> \n'+ vaprox3Coord\
                    +'\n' + vaprox5Coord +'\n\
                    </coordinates>\n\
                    </LineString>\n\
                    </Placemark>'

        bordeAproxPista2I='<Placemark> \n\
                    <description>RWYLD</description> \n\
                    <styleUrl>#line1</styleUrl> \n\
                    <LineString> \n\
                    <altitudeMode>absolute</altitudeMode> \n\
                    <extrude>0</extrude> \n\
                    <coordinates> \n'+ vaprox4Coord\
                    +'\n' + vaprox6Coord +'\n\
                    </coordinates>\n\
                    </LineString>\n\
                    </Placemark>'
           
        # Area de Aproximacion de  pista
        areaAprox2='<Placemark>\n\
              <description>0</description>\n\
              <styleUrl>#Aprox2</styleUrl>\n\
              <Polygon>\n\
                <altitudeMode>absolute</altitudeMode>\n\
                <extrude>0</extrude>\n\
                <outerBoundaryIs>\n\
                    <LinearRing>\n\
                    <coordinates>\n'+vaprox3Coord\
                    +'\n'+vaprox4Coord\
                    +'\n'+vaprox6Coord\
                    +'\n'+vaprox5Coord\
                    +'\n'+vaprox3Coord\
                    +'\n </coordinates>\n\
                  </LinearRing>\n\
                  </outerBoundaryIs>\n\
                </Polygon>\n\
            </Placemark>'
        # ----- SECCION HORIZONTAL
        if seccionH=='nd':
            pass
        else:
            verticefinTercerasecLong1,verticefinTercerasecLat1=verticesLibre1(verticefinSEGUNDAsecLong1,verticefinSEGUNDAsecLat1,seccionH)
            # Vertices laterales del fin de la TERCERA SECCION
            semiainteriorfinalTERCERA=semiainteriorfinalsegunda+(seccionH*bdivergencia/100)
           
            vaproxinterLong7,vaproxinterLat7=verticesfranja(alfaprima,verticefinTercerasecLong1,verticefinTercerasecLat1,'d',semiainteriorfinalTERCERA)
            vaproxinterLong8,vaproxinterLat8=verticesfranja(alfaprima,verticefinTercerasecLong1,verticefinTercerasecLat1,'i',semiainteriorfinalTERCERA)
            #== Ejecucion de funcion para convertir de UTM a DEcimales para cargar en KML *** APROXIMACION *** TERCERA FUNCION***
            vaproxDecToKMLLong7,vaproxDecToKMLLat7=convertir_utm_dec(vaproxinterLong7,vaproxinterLat7,hmf,huso)
            vaproxDecToKMLLong8,vaproxDecToKMLLat8=convertir_utm_dec(vaproxinterLong8,vaproxinterLat8,hmf,huso)
       

            #DERECHA
            vaprox7Coord=str(vaproxDecToKMLLong7)+','+ str(vaproxDecToKMLLat7)+','+ str(umbralfinSEGUNDAseccion)
            #IZQUIERDA
            vaprox8Coord=str(vaproxDecToKMLLong8)+','+ str(vaproxDecToKMLLat8)+','+ str(umbralfinSEGUNDAseccion)

            # Area de APROXIMACION  ---- Cordenadas y areas de APROXIMACION TERCERA SECCION
     
            bordeAproxPista3D='<Placemark> \n\
                        <description>RWYLD</description> \n\
                        <styleUrl>#line1</styleUrl> \n\
                        <LineString> \n\
                        <altitudeMode>absolute</altitudeMode> \n\
                        <extrude>1</extrude> \n\
                        <coordinates> \n'+ vaprox5Coord\
                        +'\n' + vaprox7Coord +'\n\
                        </coordinates>\n\
                        </LineString>\n\
                        </Placemark>'

            bordeAproxPista3I='<Placemark> \n\
                        <description>RWYLD</description> \n\
                        <styleUrl>#line1</styleUrl> \n\
                        <LineString> \n\
                        <altitudeMode>absolute</altitudeMode> \n\
                        <extrude>0</extrude> \n\
                        <coordinates> \n'+ vaprox6Coord\
                        +'\n' + vaprox8Coord +'\n\
                        </coordinates>\n\
                        </LineString>\n\
                        </Placemark>'
               
            # Area de Aproximacion de  pista
            areaAprox3='<Placemark>\n\
                  <description>0</description>\n\
                  <styleUrl>#Aprox3</styleUrl>\n\
                  <Polygon>\n\
                    <altitudeMode>absolute</altitudeMode>\n\
                    <extrude>0</extrude>\n\
                    <outerBoundaryIs>\n\
                        <LinearRing>\n\
                        <coordinates>\n'+vaprox5Coord\
                        +'\n'+vaprox6Coord\
                        +'\n'+vaprox8Coord\
                        +'\n'+vaprox7Coord\
                        +'\n'+vaprox5Coord\
                        +'\n </coordinates>\n\
                      </LinearRing>\n\
                      </outerBoundaryIs>\n\
                    </Polygon>\n\
                </Placemark>'

    
    #*******************************************************************************************
    #*********************************** FIN  DE SLO - Aproximacion ****************************
    #*******************************************************************************************
#  ============================================================================================================================
    #  ============================================================================================================================
    #  !!!!!!!!!!!!!!!!!!!!!!!!!INICIO DE SUPERFICIE DE ASCENSO EN DESPEGUE !!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!
    #  ============================================================================================================================
    #  ============================================================================================================================
    #Borrar esta linea de guia
##    ,dep_distextremo,dep_divergencia,dep_anchofinal,dep_longitud,dep_pendiente
    # Funcion para trabajar la divergencia lateral
    def puntosDivergencia(pD_interior,pD_divergencia,pD_anchofinal,pD_longitud):
        dist_lado=(pD_anchofinal-pD_interior)/2
        dist_eje=dist_lado*100/pD_divergencia
        distancia_lateral=dist_lado+(pD_interior/2)
        return dist_eje,distancia_lateral

    semidep_linterior=dep_linterior/2
##    print(f'semidep_linterior: {semidep_linterior}')
   
    # ---------------- Vertices de ASCENSO sobre borde de franja--------------Pto 1 y Pto 2
    
    vascensointerLong1,vascensointerLat1=verticesfranja(alfaprima,verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,'d',semidep_linterior)
    vascensointerLong2,vascensointerLat2=verticesfranja(alfaprima,verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,'i',semidep_linterior)
##    print(f' vascensointerLong1: {vascensointerLong1} \n vascensointerLat1: {vascensointerLat1}')
##    print(f' vascensointerLong2: {vascensointerLong2} \n vascensointerLat2: {vascensointerLat2}')

    # ----- Vertices de Aproximacion  complemntarios --------
   
    # Punto central inicial sobre franja

    distancia_eje,distancia_lateral=puntosDivergencia(dep_linterior,dep_divergencia,dep_anchofinal,dep_longitud) # Obtencion de longitud donde alcanza la divergencia lateral
##    print(f' distancia_eje {distancia_eje}')
##    print(f' verticeProlongacionPistaLong2 {verticeProlongacionPistaLong2}')
##    print(f' verticeProlongacionPistaLat2 {verticeProlongacionPistaLat2}')
    vcentralAsDepsecLong1,vcentralAsDepsecLat1=verticesLibre2(verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,distancia_eje) #puntos centrales del fin de seccion donde alcanza la divegencia
##    print(f' vcentralAsDepsecLong1: {vcentralAsDepsecLong1} \n vcentralAsDepsecLat1: {vcentralAsDepsecLat1}')

    # Obtencion de cordenadas laterales desde el punto central donde se alcanza la divergencia lateral
    vdivLateralLong1,vdivLateralLat1=verticesfranja(alfaprima,vcentralAsDepsecLong1,vcentralAsDepsecLat1,'d',distancia_lateral)
    vdivLateralLong2,vdivLateralLat2=verticesfranja(alfaprima,vcentralAsDepsecLong1,vcentralAsDepsecLat1,'i',distancia_lateral)

# ------------------------------------------------------------------------------------
# ******************   CONversion de UTM a DeCimales **************
# ------------------------------------------------------------------------------------

    #== Ejecucion de funcion para convertir de UTM a Decimales del pto 1 y 2
    vAsDecLong1,vAsDecLat1=convertir_utm_dec(vascensointerLong1,vascensointerLat1,hmf,huso)
    vAsDecLong2,vAsDecLat2=convertir_utm_dec(vascensointerLong2,vascensointerLat2,hmf,huso)

    #== Ejecucion de funcion para convertir de UTM a Decimales de los puntos laterales del fin de la divergencia
    vAsDecDivergLong1,vAsDecDivergLat1=convertir_utm_dec(vdivLateralLong1,vdivLateralLat1,hmf,huso)
    vAsDecDivergLong2,vAsDecDivergLat2=convertir_utm_dec(vdivLateralLong2,vdivLateralLat2,hmf,huso)

# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

##    print(f' nClave: {nClave}')

    if combo2==1 or combo2==2:
        h_umbral2=umbral2Elev
        hf_pendiente=(distancia_eje*dep_pendiente)/100+h_umbral2
        pto_1_asc=str(vAsDecLong1)+','+ str(vAsDecLat1)+','+ str(umbral2Elev)
##        print(f' pto_1_asc: {pto_1_asc}')
        pto_2_asc=str(vAsDecLong2)+','+ str(vAsDecLat2)+','+ str(umbral2Elev)
        pto_3_asc=str(vAsDecDivergLong1)+','+ str(vAsDecDivergLat1)+','+ str(hf_pendiente)
        pto_4_asc=str(vAsDecDivergLong2)+','+ str(vAsDecDivergLat2)+','+ str(hf_pendiente)
        ptos_area_ASC= pto_1_asc +'\n'+pto_2_asc +'\n'+pto_4_asc +'\n'+pto_3_asc+'\n'+pto_1_asc # Armando de puntos con cordenadas en Decimales
        
    elif combo2==3 or combo2==4:
        h_umbral2=umbral2Elev
##        print(f' h_umbral2: {h_umbral2}')
        hf_pendiente=(distancia_eje*dep_pendiente)/100+h_umbral2# zona sin divergencia
        hf_pendiente2=(dep_longitud*dep_pendiente)/100+h_umbral2
        distancia_eje2=dep_longitud-distancia_eje
        VLong1,VLat1=verticesLibre2(vdivLateralLong1,vdivLateralLat1,distancia_eje2)# Obteniendo los puntos finales rectos desde el fin de punto de divergncia: (vdivLateralLong1,vdivLateralLat1) (vdivLateralLong2,vdivLateralLat2)
        VLong2,VLat2=verticesLibre2(vdivLateralLong2,vdivLateralLat2,distancia_eje2)# Punto final 1
        vAs_final_Long1,vAs_final_Lat1=convertir_utm_dec(VLong1,VLat1,hmf,huso)#conversion de UTM a Decimales
        vAs_final_Long2,vAs_final_Lat2=convertir_utm_dec(VLong2,VLat2,hmf,huso)
        pto_1_asc=str(vAsDecLong1)+','+ str(vAsDecLat1)+','+ str(umbral2Elev)# Armando de puntos con cordenadas en Decimales
##        print(f' pto_1_asc: {pto_1_asc}')
        pto_2_asc=str(vAsDecLong2)+','+ str(vAsDecLat2)+','+ str(umbral2Elev)
        pto_3_asc=str(vAsDecDivergLong1)+','+ str(vAsDecDivergLat1)+','+ str(hf_pendiente)
        pto_4_asc=str(vAsDecDivergLong2)+','+ str(vAsDecDivergLat2)+','+ str(hf_pendiente)
        pto_5_asc=str(vAs_final_Long1)+','+ str(vAs_final_Lat1)+','+ str(hf_pendiente2)
        pto_6_asc=str(vAs_final_Long2)+','+ str(vAs_final_Lat2)+','+ str(hf_pendiente2)
        ptos_area_ASC= pto_1_asc+'\n'+pto_2_asc+'\n'+pto_4_asc+'\n'+pto_6_asc+'\n'+pto_5_asc+'\n'+pto_3_asc+'\n'+pto_1_asc

        # Area de ASCENSO en despegue


    areaASC='<Placemark>\n\
          <description>0</description>\n\
          <styleUrl>#ASC</styleUrl>\n\
          <Polygon>\n\
            <altitudeMode>absolute</altitudeMode>\n\
            <extrude>0</extrude>\n\
            <outerBoundaryIs>\n\
                <LinearRing>\n\
                <coordinates>\n'+ptos_area_ASC\
                +'\n </coordinates>\n\
              </LinearRing>\n\
              </outerBoundaryIs>\n\
          </Polygon>\n\
          </Placemark>'
    

##    

    # ============================================================================================================
    #  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!FIN SUPERFICIE DE ASCENSO EN DESPEGUE !!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!
    # ============================================================================================================


    
    #======================================================================================================================================
    # Estas lineas de ARP sirven para la SHI y para la superficie de TRANSICION antes estaban solo en la SHI solamente
    #======================================================================================================================================
    #hi_radio
    if var==0:
        ARP=umbral1Elev

    elif var==1:
        ARP=umbral2Elev

    elif var==2:
        ARP=(umbral2Elev+umbral1Elev)/2
    
    #*******************************************************************************************
    #*********************************** SUPERFICIE TRANSICION*************************
    #*******************************************************************************************
    tran_pendiente
    
    h_op=umbral1Elev

    hop_franja=45+ARP-h_op #
    
##    print(f' hop_franja: {hop_franja}')
    dop=hop_franja/(mprim/100)
    #print(f' dop: {dop}')

    if dop<=distprimer:
        doperacion=dop
        tran_central_Long1,tran_central_Lat1=verticesLibre1( verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,doperacion)

        d_lateral=(ainterior/2)+(bdivergencia*doperacion/100)
        
        tran_laterald_Long1,tran_laterald_Lat1=verticesfranja(alfaprima,tran_central_Long1,tran_central_Lat1,'d',d_lateral)
        tran_laterali_Long1,tran_laterali_Lat1=verticesfranja(alfaprima,tran_central_Long1,tran_central_Lat1,'i',d_lateral)

        ##En linea de franja 1 OP
          #h_tran_franja=hop_franja
        
        d_pendiente_tran=45/(tran_pendiente/100)#hop_franja en lugar del 45 para probar

        dlatetal_franja=(ainterior/2)+d_pendiente_tran


        tran_lateral_franjad_Long1,tran_lateral_franjad_Lat1=verticesfranja(alfaprima,verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,'d',dlatetal_franja)
        tran_lateral_franjai_Long1,tran_lateral_franjai_Lat1=verticesfranja(alfaprima,verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,'i',dlatetal_franja)
        
        # para el extremo
        tran_central_Long2,tran_central_Lat2=verticesLibre2( verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,doperacion)
        #En linea de franja 2 Extremo
        tran_lateral_franjad_Long2,tran_lateral_franjad_Lat2=verticesfranja(alfaprima, verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,'d',dlatetal_franja)
        tran_lateral_franjai_Long2,tran_lateral_franjai_Lat2=verticesfranja(alfaprima, verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,'i',dlatetal_franja)

        
    elif dop>distprimer:
        doperacion=dop
        dop1=distprimer
        hop2=distprimer*mprim/100
        hopf=hop_franja-hop2
        dop2=hopf*100/msegunda
        d_lateral=(b/2)+(bdivergencia*doperacion/100)
        tran_central_Long1,tran_central_Lat1=verticesLibre1( verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,distprimer)
        tran_central2_Long1,tran_central2_Lat1=verticesLibre1(tran_central_Long1,tran_central_Lat1,dop2)
        
        tran_laterald_Long1,tran_laterald_Lat1=verticesfranja(alfaprima,tran_central2_Long1,tran_central2_Lat1,'d',d_lateral)
        tran_laterali_Long1,tran_laterali_Lat1=verticesfranja(alfaprima,tran_central2_Long1,tran_central2_Lat1,'i',d_lateral)
  
        #En linea de franja 1 OP
        h_tran_franja=hop_franja
        d_pendiente_tran=h_tran_franja/(tran_pendiente/100)
        dlatetal_franja=d_lateral+d_pendiente_tran
        tran_lateral_franjad_Long1,tran_lateral_franjad_Lat1=verticesfranja(alfaprima,verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,'d',dlatetal_franja)
        tran_lateral_franjai_Long1,tran_lateral_franjai_Lat1=verticesfranja(alfaprima,verticeProlongacionPistaLong1,verticeProlongacionPistaLat1,'i',dlatetal_franja)
        
        # para el extremo
        tran_central_Long2,tran_central_Lat2=verticesLibre2( verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,doperacion)
        #En linea de franja 2 Extremo
        tran_lateral_franjad_Long2,tran_lateral_franjad_Lat2=verticesfranja(alfaprima,verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,'d',dlatetal_franja)
        tran_lateral_franjai_Long2,tran_lateral_franjai_Lat2=verticesfranja(alfaprima,verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,'i',dlatetal_franja)
# ------------------------------------------------------------------------------------
# ******************   CONversion de UTM a DeCimales **************
# ------------------------------------------------------------------------------------

    #== Ejecucion de funcion para convertir de UTM a Decimales DERECHO
    tran_Dec_Long1,tran_Dec_Lat1=convertir_utm_dec(tran_laterald_Long1,tran_laterald_Lat1,hmf,huso)
    tran_Dec_Long2,tran_Dec_Lat2=convertir_utm_dec(tran_lateral_franjad_Long1,tran_lateral_franjad_Lat1,hmf,huso)
    tran_Dec_Long3,tran_Dec_Lat3=convertir_utm_dec(tran_lateral_franjad_Long2,tran_lateral_franjad_Lat2,hmf,huso)

    #== Ejecucion de funcion para convertir de UTM a Decimales Izquierdo
    tran_Dec_Long4,tran_Dec_Lat4=convertir_utm_dec(tran_laterali_Long1,tran_laterali_Lat1,hmf,huso)
    tran_Dec_Long5,tran_Dec_Lat5=convertir_utm_dec(tran_lateral_franjai_Long1,tran_lateral_franjai_Lat1,hmf,huso)
    tran_Dec_Long6,tran_Dec_Lat6=convertir_utm_dec(tran_lateral_franjai_Long2,tran_lateral_franjai_Lat2,hmf,huso)    

 
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

    pto_1_tran=str(tran_Dec_Long1)+','+ str(tran_Dec_Lat1)+','+ str(hop_franja+umbral1Elev)
    pto_2_tran=str(tran_Dec_Long2)+','+ str(tran_Dec_Lat2)+','+ str(hop_franja+umbral1Elev)
    pto_3_tran=str(tran_Dec_Long3)+','+ str(tran_Dec_Lat3)+','+ str(hop_franja+umbral1Elev)
    pto_d4_tran=vfranja2Coord
    pto_d5_tran=vfranja1Coord
    
    
    
    pto_4_tran=str(tran_Dec_Long4)+','+ str(tran_Dec_Lat4)+','+ str(hop_franja+umbral1Elev)
    pto_5_tran=str(tran_Dec_Long5)+','+ str(tran_Dec_Lat5)+','+ str(hop_franja+umbral1Elev)
    pto_6_tran=str(tran_Dec_Long6)+','+ str(tran_Dec_Lat6)+','+ str(hop_franja+umbral1Elev)
    pto_i7_tran=vfranja4Coord
    pto_i8_tran=vfranja3Coord
    
    ptos_area_tranD= pto_1_tran +'\n'+pto_2_tran +'\n'+pto_3_tran +'\n'+pto_d4_tran+'\n'+pto_d5_tran+'\n'+pto_1_tran # Armando de puntos con cordenadas en Decimales
    ptos_area_tranI= pto_4_tran +'\n'+pto_5_tran +'\n'+pto_6_tran +'\n'+pto_i7_tran+'\n'+pto_i8_tran+'\n'+pto_4_tran
    
    #Puntos para la SHI en el ascenso en el despegue
    pto_interno_asc1=str(vAsDecLong1)+','+str(vAsDecLat1)+','+str(hop_franja+umbral1Elev)
    pto_interno_asc2=str(vAsDecLong2)+','+str(vAsDecLat2)+','+str(hop_franja+umbral1Elev)
    dist_lateral_asc=((45+ARP-umbral2Elev)*(dep_divergencia/dep_pendiente))+(dep_linterior/2)# ecuacion simplificada para la distancia lateral respecto del eje en funcion de pendiente y divergencia 
    # Punto central a la longitud final respecto del inicio de la sup de asc despegue donde se alcanza los 45 m
    longitud_asc=(45+ARP-umbral2Elev)*(100/dep_pendiente)
    lateral_asc=longitud_asc*dep_divergencia/100

    pto45_central_Long,pto45_central_Lat=verticesLibre2(verticeProlongacionPistaLong2,verticeProlongacionPistaLat2,longitud_asc)# funcion para encontrar el punto central

    asc_Long1,asc_Lat1=verticesfranja(alfaprima,pto45_central_Long,pto45_central_Lat,'d',dist_lateral_asc)#para encontrar los puntos laterales finales 
    asc_Long2,asc_Lat2=verticesfranja(alfaprima,pto45_central_Long,pto45_central_Lat,'i',dist_lateral_asc)
    #  Convirtiendo de UTM a DEC:
    dec_asc_Long1,dec_asc_Lat1=convertir_utm_dec(asc_Long1,asc_Lat1,hmf,huso)
    dec_asc_Long2,dec_asc_Lat2=convertir_utm_dec(asc_Long2,asc_Lat2,hmf,huso)
    # ELEVACION DEL PUNTO FINAL
    elev45=45+ARP
    
    pto_asc1=str(dec_asc_Long1)+','+str(dec_asc_Lat1)+','+str(elev45)
    pto_asc2=str(dec_asc_Long2)+','+str(dec_asc_Lat2)+','+str(elev45)


    #Puntos internos para La SUPERFICIE HORIZONTAL INTERNA
    ptos_internos_SHI=pto_1_tran +'\n'+pto_2_tran +'\n'+pto_3_tran +'\n'+pto_interno_asc1+'\n'+pto_asc1+'\n'+pto_asc2+'\n'+pto_interno_asc2+'\n'+pto_6_tran+'\n'+pto_5_tran+'\n'+pto_4_tran+'\n'+pto_1_tran
##    ptos_internos_SHI=pto_1_tran +'\n'+pto_2_tran +'\n'+pto_3_tran +'\n'+pto_interno_asc1+'\n'+pto_asc1+'\n'+pto_asc1p+'\n'+pto_asc2p+'\n'+pto_asc2+'\n'+pto_interno_asc2+'\n'+pto_6_tran+'\n'+pto_5_tran+'\n'+pto_4_tran+'\n'+pto_1_tran
    ##ptos_internos_SHI=pto_1_tran +'\n'+pto_2_tran +'\n'+pto_3_tran +'\n'+pto_6_tran+'\n'+pto_5_tran+'\n'+pto_4_tran+'\n'+pto_1_tran


        # Area de TRANSICION DERECHA

    areaTRAND='<Placemark>\n\
          <description>0</description>\n\
          <styleUrl>#TRAN</styleUrl>\n\
          <Polygon>\n\
            <altitudeMode>absolute</altitudeMode>\n\
            <extrude>0</extrude>\n\
            <outerBoundaryIs>\n\
                <LinearRing>\n\
                <coordinates>\n'+ptos_area_tranD\
                +'\n </coordinates>\n\
              </LinearRing>\n\
              </outerBoundaryIs>\n\
          </Polygon>\n\
          </Placemark>'
      # Area TRANSICION iZQUIRDA


    areaTRANI='<Placemark>\n\
          <description>0</description>\n\
          <styleUrl>#TRAN</styleUrl>\n\
          <Polygon>\n\
            <altitudeMode>absolute</altitudeMode>\n\
            <extrude>0</extrude>\n\
            <outerBoundaryIs>\n\
                <LinearRing>\n\
                <coordinates>\n'+ptos_area_tranI\
                +'\n </coordinates>\n\
              </LinearRing>\n\
              </outerBoundaryIs>\n\
          </Polygon>\n\
          </Placemark>'
   
    #*******************************************************************************************
    #*********************************** FIN SUPERFICIE TRANSICION *************************
    #*******************************************************************************************

    
    #=====================================================================================================================================
    #=====================================================================================================================================
    
    
    #*******************************************************************************************
    #*********************************** SUPERFICIE HORIZONTAL INTERNA *************************
    #*******************************************************************************************

    # --------------   SEMI- CIRCUNFERENCIA PUNTO 2 (DERECHA)  ------------------
    
    hi_altura_final=hi_altura+ARP
    #print(f' hi_altura_final: {hi_altura_final}')
    cir_der=[]
    cir_der1=[]
    #cir1r=[]

    if P1Long>P2Long:
        mpendiente=(P2Lat-P1Lat)/(P2Long-P1Long)
        if mpendiente<0:# Listo probado en P Este 
##            print(f' P2Long<P1Long || pendiente <0')
##            print(azimut)
##            print(azimut-180)
            azimut1=(azimut-180)
            ang_cir_der1=90
            ang_cir_der2=-90
            ang_cir_der3=90
            ang_cir_der4=270
            for v in range(ang_cir_der2,ang_cir_der1,1):
                c1=(P2Lat+hi_radio*math.cos(math.radians(azimut1+v)))
                c2=(P2Long+hi_radio*math.sin(math.radians(azimut1+v)))
                c3=(hi_altura_final)
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(c2,c1,hmf,huso)
                c=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(c3)
                cir_der.append(c)
                p_folder_circ = "\n".join(cir_der)#p_folder_circ=str(cir_der)[1:-1]
                p_folder_circ2=p_folder_circ.replace("',","")
                p_folder_circ3=p_folder_circ2.replace("'","")
            for v in range(ang_cir_der3,ang_cir_der4,1):
                c1=(P1Lat+hi_radio*math.cos(math.radians(azimut1+v)))
                c2=(P1Long+hi_radio*math.sin(math.radians(azimut1+v)))
                c3=(hi_altura_final)
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(c2,c1,hmf,huso)
                c=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(c3)
                print(c)
                cir_der1.append(c)
                p_folder_circ1 = "\n".join(cir_der1)#p_folder_circ1=str(cir_der1)[1:-1]
                p_folder_circ21=p_folder_circ1.replace("',","")
                p_folder_circ31=p_folder_circ21.replace("'","")
##                print(f' aqui-')
        elif mpendiente>0: # Listo probado en P Este 
##            print(f' P2Long<P1Long || pendiente >0')
            azimut1=-1*(azimut-90)
            ang_cir_der1=90
            ang_cir_der2=270
            ang_cir_der3=-90
            ang_cir_der4=90
##            print(f' aqui+')
            for v in range(ang_cir_der1,ang_cir_der2,1):
                c1=P2Lat+hi_radio*math.sin(math.radians(azimut1+v))
                c2=P2Long+hi_radio*math.cos(math.radians(azimut1+v))
                c3=hi_altura_final
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(c2,c1,hmf,huso)
                c=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(c3)
                cir_der.append(c)
                p_folder_circ = "\n".join(cir_der)#p_folder_circ=str(cir_der)[1:-1]
                p_folder_circ2=p_folder_circ.replace("',","")
                p_folder_circ3=p_folder_circ2.replace("'","")
            for v in range(ang_cir_der3,ang_cir_der4,1):
                c1=P1Lat+hi_radio*math.sin(math.radians(azimut1+v))
                c2=P1Long+hi_radio*math.cos(math.radians(azimut1+v))
                c3=hi_altura_final
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(c2,c1,hmf,huso)
                c=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(c3)
                cir_der1.append(c)
                p_folder_circ1 = "\n".join(cir_der1)#p_folder_circ1=str(cir_der1)[1:-1]
                p_folder_circ21=p_folder_circ1.replace("',","")
                p_folder_circ31=p_folder_circ21.replace("'","")

    elif P2Long>P1Long: # listo aplicado en punta del Este
        mpendiente=(P1Lat-P2Lat)/(P1Long-P2Long)
        if mpendiente<0:
##            print(f' P2Long>P1Long || pendiente <0')
            azimut1=-1*(azimut-90)
            ang_cir_der1=-90
            ang_cir_der2=90
            ang_cir_der3=90
            ang_cir_der4=270
            for v in range(ang_cir_der1,ang_cir_der2,1):
                c1=P2Lat+hi_radio*math.sin(math.radians(azimut1+v))
                c2=P2Long+hi_radio*math.cos(math.radians(azimut1+v))
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(c2,c1,hmf,huso)
                c=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(hi_altura_final)
                cir_der.append(c)
                p_folder_circ = "\n".join(cir_der)#p_folder_circ=str(cir_der)[1:-1]
                p_folder_circ2=p_folder_circ.replace("',","")
                p_folder_circ3=p_folder_circ2.replace("'","")
            for v in range(ang_cir_der3,ang_cir_der4,1):
                c1=P1Lat+hi_radio*math.sin(math.radians(azimut1+v))
                c2=P1Long+hi_radio*math.cos(math.radians(azimut1+v))
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(c2,c1,hmf,huso)
                c=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(hi_altura_final)
                cir_der1.append(c)
                p_folder_circ1 = "\n".join(cir_der1)#p_folder_circ1=str(cir_der1)[1:-1]
                p_folder_circ21=p_folder_circ1.replace("',","")
                p_folder_circ31=p_folder_circ21.replace("'","")
               
        elif mpendiente>0: # Listo aplicado a punta del Este 

            azimut1=90-azimut
            ang_cir_der1=90
            ang_cir_der2=-90
            ang_cir_der3=90
            ang_cir_der4=270
            for v in range(ang_cir_der2,ang_cir_der1,1):
                c1=P2Lat+hi_radio*math.sin(math.radians(azimut1+v))
                c2=P2Long+hi_radio*math.cos(math.radians(azimut1+v))
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(c2,c1,hmf,huso)
                c=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(hi_altura_final)
                cir_der.append(c)
                p_folder_circ = "\n".join(cir_der)#p_folder_circ=str(cir_der)[1:-1]
                p_folder_circ2=p_folder_circ.replace("',","")
                p_folder_circ3=p_folder_circ2.replace("'","")
            for v in range(ang_cir_der3,ang_cir_der4,1):
                c1=P1Lat+hi_radio*math.sin(math.radians(azimut1+v))
                c2=P1Long+hi_radio*math.cos(math.radians(azimut1+v))
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(c2,c1,hmf,huso)
                c=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(hi_altura_final)
                cir_der1.append(c)# append sirve para añADIR elemento al final de la lista 
                p_folder_circ1 = "\n".join(cir_der1)#p_folder_circ1=str(cir_der1)[1:-1]
                p_folder_circ21=p_folder_circ1.replace("',","")
                p_folder_circ31=p_folder_circ21.replace("'","")
               

    # Area Superficie Horizontal Interna 
    Sup_HI=p_folder_circ3+'\n'+p_folder_circ31+'\n'+p_folder_circ3.split("\n")[0]  #p_folder_circ3[0:25]
    #print(f" p_folder_circ3: {p_folder_circ3[0:25]}")

             
##    SHI='<Placemark> \n\
##        <description>RWYLD</description> \n\
##        <styleUrl>#line1</styleUrl> \n\
##        <LineString> \n\
##        <altitudeMode>absolute</altitudeMode> \n\
##        <extrude>1</extrude> \n\
##        <coordinates> \n'+Sup_HI+'\n\
##        </coordinates>\n\
##        </LineString>\n\
##        </Placemark>'
# Area de Aproximacion de  pista
    SHI='<Placemark>\n\
                  <description>0</description>\n\
                  <styleUrl>#HI</styleUrl>\n\
                  <Polygon>\n\
                    <altitudeMode>absolute</altitudeMode>\n\
                    <extrude>1</extrude>\n\
                    <outerBoundaryIs>\n\
                        <LinearRing>\n\
                        <coordinates>\n'+Sup_HI\
                        +'\n </coordinates>\n\
                      </LinearRing>\n\
                      </outerBoundaryIs>\n\
                      <innerBoundaryIs>\n\
                   <LinearRing>\n\
                    <coordinates>\n'+ ptos_internos_SHI\
                    +'\n </coordinates>\n\
                    </LinearRing>\n\
                      </innerBoundaryIs>\n\
                    </Polygon>\n\
                    </Placemark>'

           
   
    #*******************************************************************************************
    #*********************************** FUN DE LA SUPERFICIE HORIZONTAL INTERNA ***************
    #*******************************************************************************************


    
#***************************************************************************************************************
#***************************************************************************************************************

#*********************************** SUPERFICIE CONICA *************************
    #*******************************************************************************************

    # --------------   SEMI- CIRCUNFERENCIA PUNTO 2 (DERECHA)  ------------------

    hi_altura_final = hi_altura + ARP
    c_hi_radio = hi_radio + (100 / c_pendiente) * c_altura
    cir_der = []
    cir_der1 = []

    if P1Long>P2Long:
        mpendiente=(P2Lat-P1Lat)/(P2Long-P1Long)
        if mpendiente<0:# Listo probado en P Este 
##            print(f' P2Long<P1Long || pendiente <0')
##            print(azimut)
##            print(azimut-180)
            azimut1=(azimut-180)
            ang_cir_derc1=90
            ang_cir_derc2=-90
            ang_cir_derc3=90
            ang_cir_derc4=270
            for v in range(ang_cir_derc2,ang_cir_derc1,1):
                cc1=(P2Lat+c_hi_radio*math.cos(math.radians(azimut1+v)))
                cc2=(P2Long+c_hi_radio*math.sin(math.radians(azimut1+v)))
                cc3=(hi_altura_final+c_altura)
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(cc2,cc1,hmf,huso)
                cc=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(cc3)
                cir_der.append(cc)
                c_folder_circ = "\n".join(cir_der)#c_folder_circ=str(cir_der)[1:-1]
                c_folder_circ2=c_folder_circ.replace("',","")
                c_folder_circ3=c_folder_circ2.replace("'","")
            for v in range(ang_cir_derc3,ang_cir_derc4,1):
                cc1=(P1Lat+c_hi_radio*math.cos(math.radians(azimut1+v)))
                cc2=(P1Long+c_hi_radio*math.sin(math.radians(azimut1+v)))
                cc3=(hi_altura_final+c_altura)
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(cc2,cc1,hmf,huso)
                cc=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(cc3)
                #print(c)
                cir_der1.append(cc)
                c_folder_circ1 = "\n".join(cir_der1)#c_folder_circ1=str(cir_der1)[1:-1]
                c_folder_circ21=c_folder_circ1.replace("',","")
                c_folder_circ31=c_folder_circ21.replace("'","")
##                print(f' aqui-')
        elif mpendiente>0: # Listo probado en P Este 
##            print(f' P2Long<P1Long || pendiente >0')
            azimut1=-1*(azimut-90)
            ang_cir_derc1=90
            ang_cir_derc2=270
            ang_cir_derc3=-90
            ang_cir_derc4=90
##            print(f' aqui+')
            for v in range(ang_cir_derc1,ang_cir_derc2,1):
                cc1=P2Lat+c_hi_radio*math.sin(math.radians(azimut1+v))
                cc2=P2Long+c_hi_radio*math.cos(math.radians(azimut1+v))
                cc3=(hi_altura_final+c_altura)
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(cc2,cc1,hmf,huso)
                cc=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(cc3)
                cir_der.append(cc)
                c_folder_circ = "\n".join(cir_der)#c_folder_circ=str(cir_der)[1:-1]
                c_folder_circ2=c_folder_circ.replace("',","")
                c_folder_circ3=c_folder_circ2.replace("'","")
            for v in range(ang_cir_derc3,ang_cir_derc4,1):
                cc1=P1Lat+c_hi_radio*math.sin(math.radians(azimut1+v))
                cc2=P1Long+c_hi_radio*math.cos(math.radians(azimut1+v))
                cc3=(hi_altura_final+c_altura)
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(cc2,cc1,hmf,huso)
                cc=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(cc3)
                cir_der1.append(cc)
                c_folder_circ1 = "\n".join(cir_der1)#c_folder_circ1=str(cir_der1)[1:-1]
                c_folder_circ21=c_folder_circ1.replace("',","")
                c_folder_circ31=c_folder_circ21.replace("'","")

    elif P2Long>P1Long: # listo aplicado en punta del Este
        mpendiente=(P1Lat-P2Lat)/(P1Long-P2Long)
        if mpendiente<0:
##            print(f' P2Long>P1Long || pendiente <0')
            azimut1=-1*(azimut-90)
            ang_cir_derc1=-90
            ang_cir_derc2=90
            ang_cir_derc3=90
            ang_cir_derc4=270
            for v in range(ang_cir_derc1,ang_cir_derc2,1):
                cc1=P2Lat+c_hi_radio*math.sin(math.radians(azimut1+v))
                cc2=P2Long+c_hi_radio*math.cos(math.radians(azimut1+v))
                cc3=(hi_altura_final+c_altura)
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(cc2,cc1,hmf,huso)
                cc=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(cc3)
                cir_der.append(cc)
                c_folder_circ = "\n".join(cir_der)#c_folder_circ=str(cir_der)[1:-1]
                c_folder_circ2=c_folder_circ.replace("',","")
                c_folder_circ3=c_folder_circ2.replace("'","")
            for v in range(ang_cir_derc3,ang_cir_derc4,1):
                cc1=P1Lat+c_hi_radio*math.sin(math.radians(azimut1+v))
                cc2=P1Long+c_hi_radio*math.cos(math.radians(azimut1+v))
                cc3=(hi_altura_final+c_altura)
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(cc2,cc1,hmf,huso)
                cc=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(cc3)
                cir_der1.append(cc)
                c_folder_circ1 = "\n".join(cir_der1)#c_folder_circ1=str(cir_der1)[1:-1]
                c_folder_circ21=c_folder_circ1.replace("',","")
                c_folder_circ31=c_folder_circ21.replace("'","")
               
        elif mpendiente>0: # Listo aplicado a punta del Este 
##            print(f' P2Long>P1Long || pendiente >0')
            azimut1=90-azimut
            ang_cir_derc1=90
            ang_cir_derc2=-90
            ang_cir_derc3=90
            ang_cir_derc4=270
            for v in range(ang_cir_derc2,ang_cir_derc1,1):
                cc1=P2Lat+c_hi_radio*math.sin(math.radians(azimut1+v))
                cc2=P2Long+c_hi_radio*math.cos(math.radians(azimut1+v))
                cc3=(hi_altura_final+c_altura)
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(cc2,cc1,hmf,huso)
                cc=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(cc3)
                cir_der.append(cc)
                c_folder_circ = "\n".join(cir_der)#c_folder_circ=str(cir_der)[1:-1]
                c_folder_circ2=c_folder_circ.replace("',","")
                c_folder_circ3=c_folder_circ2.replace("'","")
            for v in range(ang_cir_derc3,ang_cir_derc4,1):
                cc1=P1Lat+c_hi_radio*math.sin(math.radians(azimut1+v))
                cc2=P1Long+c_hi_radio*math.cos(math.radians(azimut1+v))
                cc3=(hi_altura_final+c_altura)
                UTMtoDecLong,UTMtoDecLat=convertir_utm_dec(cc2,cc1,hmf,huso)
                cc=str(UTMtoDecLong)+','+str(UTMtoDecLat)+','+str(cc3)
                cir_der1.append(cc)# append sirve para añADIR elemento al final de la lista 
                c_folder_circ1 = "\n".join(cir_der1)#c_folder_circ1=str(cir_der1)[1:-1]
                c_folder_circ21=c_folder_circ1.replace("',","")
                c_folder_circ31=c_folder_circ21.replace("'","")
               

    # Area Superficie Horizontal Interna 
    Sup_C=c_folder_circ3+'\n'+c_folder_circ31+'\n'+c_folder_circ3.split("\n")[0]

##    if P1Long > P2Long:
##        mpendiente = (P2Lat - P1Lat) / (P2Long - P1Long)
##        if mpendiente < 0:  # Probado en Punta del Este
##            azimut1 = azimut - 180
##            ang_cir_derc1, ang_cir_derc2 = 90, -90
##            ang_cir_derc3, ang_cir_derc4 = 90, 270
##            
##            for v in range(ang_cir_derc2, ang_cir_derc1, 1):
##                cc1 = P2Lat + c_hi_radio * math.cos(math.radians(azimut1 + v))
##                cc2 = P2Long + c_hi_radio * math.sin(math.radians(azimut1 + v))
##                cc3 = hi_altura_final + c_altura
##                UTMtoDecLong, UTMtoDecLat = convertir_utm_dec(cc2, cc1, hmf, huso)
##                cc = f"{UTMtoDecLong},{UTMtoDecLat},{cc3}"
##                cir_der.append(cc)
##            
##            for v in range(ang_cir_derc3, ang_cir_derc4, 1):
##                cc1 = P1Lat + c_hi_radio * math.cos(math.radians(azimut1 + v))
##                cc2 = P1Long + c_hi_radio * math.sin(math.radians(azimut1 + v))
##                cc3 = hi_altura_final + c_altura
##                UTMtoDecLong, UTMtoDecLat = convertir_utm_dec(cc2, cc1, hmf, huso)
##                cc = f"{UTMtoDecLong},{UTMtoDecLat},{cc3}"
##                cir_der1.append(cc)
##
##        elif mpendiente > 0:  # Probado en Punta del Este
##            azimut1 = -(azimut - 90)
##            ang_cir_derc1, ang_cir_derc2 = 90, 270
##            ang_cir_derc3, ang_cir_derc4 = -90, 90
##
##            for v in range(ang_cir_derc1, ang_cir_derc2, 1):
##                cc1 = P2Lat + c_hi_radio * math.sin(math.radians(azimut1 + v))
##                cc2 = P2Long + c_hi_radio * math.cos(math.radians(azimut1 + v))
##                cc3 = hi_altura_final + c_altura
##                UTMtoDecLong, UTMtoDecLat = convertir_utm_dec(cc2, cc1, hmf, huso)
##                cc = f"{UTMtoDecLong},{UTMtoDecLat},{cc3}"
##                cir_der.append(cc)
##
##            for v in range(ang_cir_derc3, ang_cir_derc4, 1):
##                cc1 = P1Lat + c_hi_radio * math.sin(math.radians(azimut1 + v))
##                cc2 = P1Long + c_hi_radio * math.cos(math.radians(azimut1 + v))
##                cc3 = hi_altura_final + c_altura
##                UTMtoDecLong, UTMtoDecLat = convertir_utm_dec(cc2, cc1, hmf, huso)
##                cc = f"{UTMtoDecLong},{UTMtoDecLat},{cc3}"
##                cir_der1.append(cc)
##
##    elif P2Long > P1Long:  # Aplicado en Punta del Este
##        mpendiente = (P1Lat - P2Lat) / (P1Long - P2Long)
##        if mpendiente < 0:
##            azimut1 = -(azimut - 90)
##            ang_cir_derc1, ang_cir_derc2 = -90, 90
##            ang_cir_derc3, ang_cir_derc4 = 90, 270
##
##            for v in range(ang_cir_derc1, ang_cir_derc2, 1):
##                cc1 = P2Lat + c_hi_radio * math.sin(math.radians(azimut1 + v))
##                cc2 = P2Long + c_hi_radio * math.cos(math.radians(azimut1 + v))
##                cc3 = hi_altura_final + c_altura
##                UTMtoDecLong, UTMtoDecLat = convertir_utm_dec(cc2, cc1, hmf, huso)
##                cc = f"{UTMtoDecLong},{UTMtoDecLat},{cc3}"
##                cir_der.append(cc)
##
##            for v in range(ang_cir_derc3, ang_cir_derc4, 1):
##                cc1 = P1Lat + c_hi_radio * math.sin(math.radians(azimut1 + v))
##                cc2 = P1Long + c_hi_radio * math.cos(math.radians(azimut1 + v))
##                cc3 = hi_altura_final + c_altura
##                UTMtoDecLong, UTMtoDecLat = convertir_utm_dec(cc2, cc1, hmf, huso)
##                cc = f"{UTMtoDecLong},{UTMtoDecLat},{cc3}"
##                cir_der1.append(cc)
##
##        elif mpendiente > 0:
##            azimut1 = 90 - azimut
##            ang_cir_derc1, ang_cir_derc2 = -90, 90
##            ang_cir_derc3, ang_cir_derc4 = 90, 270
##
##            for v in range(ang_cir_derc2, ang_cir_derc1, 1):
##                cc1 = P2Lat + c_hi_radio * math.sin(math.radians(azimut1 + v))
##                cc2 = P2Long + c_hi_radio * math.cos(math.radians(azimut1 + v))
##                cc3 = hi_altura_final + c_altura
##                UTMtoDecLong, UTMtoDecLat = convertir_utm_dec(cc2, cc1, hmf, huso)
##                cc = f"{UTMtoDecLong},{UTMtoDecLat},{cc3}"
##                cir_der.append(cc)
##
##            for v in range(ang_cir_derc3, ang_cir_derc4, 1):    
##                cc1 = P1Lat + c_hi_radio * math.sin(math.radians(azimut1 + v))
##                cc2 = P1Long + c_hi_radio * math.cos(math.radians(azimut1 + v))
##                cc3 = hi_altura_final + c_altura
##                UTMtoDecLong, UTMtoDecLat = convertir_utm_dec(cc2, cc1, hmf, huso)
##                cc = f"{UTMtoDecLong},{UTMtoDecLat},{cc3}"
##                cir_der1.append(cc)
##    # Crear cadenas finales
##    c_folder_circ = ",".join(cir_der)
##    c_folder_circ1 = ",".join(cir_der1)
##
##    # Concatenar las variables si es necesario para generar la variable final
##    Sup_C = f"{c_folder_circ} {c_folder_circ1} {c_folder_circ[:25]}"

                  


# Area de Aproximacion de  pista
    SC='<Placemark>\n\
                  <description>0</description>\n\
                  <styleUrl>#C</styleUrl>\n\
                  <Polygon>\n\
                    <altitudeMode>absolute</altitudeMode>\n\
                    <extrude>0</extrude>\n\
                    <outerBoundaryIs>\n\
                        <LinearRing>\n\
                        <coordinates>\n'+Sup_C\
                        +'\n </coordinates>\n\
                      </LinearRing>\n\
                      </outerBoundaryIs>\n\
                      <innerBoundaryIs>\n\
                   <LinearRing>\n\
                    <coordinates>\n'+ Sup_HI\
                    +'\n </coordinates>\n\
                    </LinearRing>\n\
                      </innerBoundaryIs>\n\
                    </Polygon>\n\
                    </Placemark>'

           
   
    #*****************************************************************************************
    #*********************************** FUN DE LA SUPERFICIE CONICA *************************
    #*****************************************************************************************
    
#********************************************************************************************************
#********************************************************************************************************

    
    #----------------------------------- APROXIMACION ------------------------------------------
#-------------------------------------------------------------------------------------------
       
    if msegunda=='nd' and distsegunda=='nd':
        areaAprox=areaAprox1
    else:
        if seccionH=='nd':
            areaAprox=areaAprox1+areaAprox2
        else:
            areaAprox=areaAprox1+areaAprox2+areaAprox3

    folder1='<Folder> \n <name>Aproximacion</name> \n <description>SLOFolder</description>\n'+SHI+'\n'+SC+'\n'+areaTRAND+'\n'+areaTRANI+'\n'+areaASC+'\n'+areaFranja\
             + '\n'+areaPista+'\n'+areaResa1+'\n'+areaResa2\
             +'\n'+ ejePista +'\n'+bordePistaD+bordePistaI\
             +'\n'+bordeResaPista1D+bordeResaPista1I\
             +'\n'+bordeResaPista2D+bordeResaPista2I\
             +'\n'+areaAprox\
             +'\n </Folder>\n'

    folder2="<Folder> \n <name>Despegue</name> \n </Folder>\n"
    folder3="<Folder> \n <name>transicion</name> \n </Folder>\n"
    nombre=nombreaerop+nombrepista
    nombreArchivo='<name>'+ nombre +'</name>'
    cuerpokml=styloColor1+folder1+folder2 +folder3
    propDocumento='<Document>\n'+nombreArchivo+'\n'+cuerpokml+'</Document>'
    cabezakml='<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n'+propDocumento
   
   
    nombreArchivo='<name>'+ nombreaerop+nombrepista +'</name>'
    propDocumento='<Document>\n'+nombreArchivo+'\n'+cuerpokml+'</Document>'
    cabezakml='<?xml version="1.0" encoding="UTF-8"?> \n <kml xmlns="http://www.opengis.net/kml/2.2">\n'+propDocumento
    documentoFinalKml=cabezakml+'\n</kml>'

    
    nombreFinal=nombreaerop+nombrepista
    return documentoFinalKml, nombreFinal


#*******************************************************************************************
#*********************************** FIN DE INFORME*****************************************
#*******************************************************************************************





#=================================================================================

def crear_genslo(nombre_ad,Pista,Longitud_OP,Latitud_OP,Elevacion_OP,Longitud_EXT,Latitud_EXT,Elevacion_EXT,ancho_Pista,t_aproximacion,n_clave,ref_SHI):
    global txt_aeropuerto,txt_pista,txt_long1,txt_lat1, txt_elev1, txt_long2,txt_lat2,txt_elev2,txt_anchoPista,combo1,combo2,combo3,var,documentoFinalKml

    #************************** CAJAS DE TEXTO ****************************************
    txt_aeropuerto=nombre_ad
    txt_pista=Pista
    txt_long1=Longitud_OP
    txt_lat1=Latitud_OP
    txt_elev1=Elevacion_OP

    txt_long2=Longitud_EXT
    txt_lat2=Latitud_EXT
    txt_elev2=Elevacion_EXT

    txt_anchoPista=ancho_Pista


    # ************************** GRUPO DE COMBOBOX  ***********************************
    # 1ro Hermisferio

    if float(txt_long1)>0:
        combo3='N'
    else:
        combo3='S'
        

    # 2do - T. Aproximacion
    if t_aproximacion=='Visual':
        combo1='Visual'
    elif t_aproximacion=='No Precision':
        combo1='No Precision'
    elif t_aproximacion=='Precision CAT I':
        combo1='Precision CAT I'
    elif t_aproximacion=='Precision CAT II o III':
        combo1='Precision CAT II o III'
    
    # 3ro Nro Clave
    if n_clave=='1':
        combo2=1
    elif n_clave=='2':
        combo2=2
    elif n_clave=='3':
        combo2=3
    elif n_clave=='4':
        combo2=4


    # ************************** GRUPO DE RButton  ***********************************
    if ref_SHI=='RWY - THR':
        var=0
    elif ref_SHI=='RWY - Extremo':
        var=1
    elif ref_SHI=='Punto Medio':
        var=2

     # ************************** Creacion de Carpetas  ***********************************

    tipoAprox=combo1
    #print(f" tipoAprox:{tipoAprox}")
    nClave=str(combo2)
    #print(combo2)
        
    if tipoAprox=='Visual':
        if nClave=='1':
            obtener(30,30,
                    60,10,1600,5,'nd','nd','nd',
                    2000,45,
                    60,30,10,380,1600,5,
                    20,
                    5,35)
        elif nClave=='2':
            obtener(60,40,
                    80,10,2500,4,'nd','nd','nd',
                    2500,45,
                    80,60,10,580,2500,4,
                    20,
                    5,55)
        elif nClave=='3':
            obtener(60,75,
                    150,10,3000,3.33,'nd','nd','nd',
                    4000,45,
                    180,60,12.5,1200,15000,2,
                    14.3,
                    5,75)
        elif nClave=='4':
            obtener(60,75,
                    150,10,3000,2.5,'nd','nd','nd',
                    4000,45,
                    180,60,12.5,1200,15000,2,
                    14.3,
                    5,100)
    elif tipoAprox=='No Precision':
        if nClave=='1':
            obtener(60,70,
                    140,15,2500,3.33,'nd','nd','nd',
                    3500,45,
                    60,30,10,380,1600,5,
                    20,
                    5,60)
        elif nClave=='2':
            obtener(60,70,
                    140,15,2500,3.33,'nd','nd','nd',
                    3500,45,
                    80,60,10,580,2500,4,
                    20,
                    5,60)
        elif nClave=='3':
            obtener(60,140,
                    280,15,3000,2,3600,2.5,8400,
                    4000,45,
                    180,60,12.5,1200,15000,2,
                    14.3,
                    5,75)
        elif nClave=='4':
            obtener(60,140,
                    280,15,3000,2,3600,2.5,8400,
                    4000,45,
                    180,60,12.5,1200,15000,2,
                    14.3,
                    5,100)
    elif tipoAprox=='Precision CAT I':
        if nClave=='1':
            obtener(60,70,
                    140,15,3000,2.5,12000,3,'nd',
                    3500,45,
                    60,30,10,380,1600,5,
                    14.3,
                    5,60)
        elif nClave=='2':
            obtener(60,70,
                    140,15,3000,2.5,12000,3,'nd',
                    3500,45,
                    80,60,10,580,2500,4,
                    14.3,
                    5,60)
        elif nClave=='3':
            obtener(60,140,
                    280,15,3000,2,3600,2.5,8400,
                    4000,45,
                    180,60,12.5,1200,15000,2,
                    14.3,
                    5,100)
        elif nClave=='4':
            obtener(60,140,
                    280,15,3000,2,3600,2.5,8400,
                    4000,45,
                    180,60,12.5,1200,15000,2,
                    14.3,
                    5,100)
    elif tipoAprox=='Precision CAT II o III':
        if nClave=='1':
            print("No hay diseño para n° clave 1 y Aproximación de precisión Cat. II o III")
        elif nClave=='2':
            print("No hay diseño para n° clave 2 y Aproximación de precisión Cat. II o III")
        elif nClave=='3':
            obtener(60,140,
                    280,15,3000,2,3600,2.5,8400,
                    4000,45,
                    180,60,12.5,1200,15000,2,
                    14.3,
                    5,100)
        elif nClave=='4':
            obtener(60,140,
                    280,15,3000,2,3600,2.5,8400,
                    4000,45,
                    180,60,12.5,1200,15000,2,
                    14.3,
                    5,100)
            

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

def dms_to_decimal(dms):
    """Convierte coordenadas DMS a decimales. Si ya están en decimales, las devuelve sin cambios."""
    try:
        # Detectar si ya está en formato decimal
        if "." in dms and not any(char in dms for char in "NSWE"):
            # Intentar convertir directamente a float (ya es decimal)
            return round(float(dms), 8)
        
        # Si no es decimal, convertir desde DMS
        dms = dms.upper().replace("°", "").replace("'", "").replace('"', "").replace(" ", "")
        hemisphere = 1  # Por defecto positivo
        if "W" in dms or "S" in dms:
            hemisphere = -1
        dms = dms.rstrip("NSEW")  # Remover caracteres de dirección para la conversión
        degrees = float(dms[:2])  # Los primeros dos caracteres son grados
        minutes = float(dms[2:4])  # Los siguientes dos son minutos
        seconds = float(dms[4:])  # El resto son segundos
        decimal = degrees + (minutes / 60) + (seconds / 3600)
        return round(decimal * hemisphere, 8)
    except Exception:
        return " "

def main():
    st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #28a745; /* Verde profesional */
        color: white; /* Texto blanco */
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }
    div.stButton > button:first-child:hover {
        background-color: #218838; /* Verde más oscuro al pasar el mouse */
    }
    </style>
    """,
    unsafe_allow_html=True)
    st.title("GENSLO beta v1.0")
    st.header("Superficies Limitadoras de Obstáculos - Según ANEXO 14 - OACI")
    st.subheader("Grupo de Transporte Aéreo (GTA) - UNLP")
    st.markdown("""
    <div style="background-color: #fc4c4c; padding: 10px; border-radius: 5px; border: 1px solid #ffffff;">
        <strong>AVISO DE SEGURIDAD:</strong> Esta herramienta está elaborada para uso de Planificación y no como uso de Proyecto.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("__Datos del Aeródromo__")
    nombre_ad = st.text_input("Nombre de Aeródromo", placeholder="Nombre sin espacios, ex: SABE, AEP, Aeroparque")
    Pista = st.text_input("Pista Seleccionada", placeholder="Indique el Numero correspondiente al THR de Pista, ex.: 19")
    ancho_Pista = st.text_input("Ancho de Pista [m]", value="", placeholder="ex.:  45.25 ")
    st.divider()

    
    
    
    # Inicializar valores en session_state si no existen
    for key in ["Latitud_OP_DMS", "Longitud_OP_DMS", "Elevacion_OP",
                "Latitud_EXT_DMS", "Longitud_EXT_DMS", "Elevacion_EXT"]:
        if key not in st.session_state:
            st.session_state[key] = ""
    
    # Botón para invertir coordenadas y elevaciones
    if st.button("Invertir Coordenadas OP ↔ EXT"):
        st.session_state["Latitud_OP_DMS"], st.session_state["Latitud_EXT_DMS"] = st.session_state["Latitud_EXT_DMS"], st.session_state["Latitud_OP_DMS"]
        st.session_state["Longitud_OP_DMS"], st.session_state["Longitud_EXT_DMS"] = st.session_state["Longitud_EXT_DMS"], st.session_state["Longitud_OP_DMS"]
        st.session_state["Elevacion_OP"], st.session_state["Elevacion_EXT"] = st.session_state["Elevacion_EXT"], st.session_state["Elevacion_OP"]
    st.divider()
    st.markdown(f"Coordenadas De Umbral de Pista {Pista}")
    #st.markdown(f" ")
    # Entrada para latitud
    col1, col2 = st.columns(2)
    with col1:
        Latitud_OP_DMS = st.text_input(label=f"Latitud - [Grados Dec. sin (°) ó DMS sin (0)]", value="", placeholder="ex.: -34.906414 / 345430.23S / 34°54'30.23''S", key="Latitud_OP_DMS")
        
                                                                                                                                        #Latitud_OP_DMS = st.text_input(f"Latitud - THR {Pista} [Grados Dec. sin (°) ó DMS sin (0)]",
                                                                                                                                          #value="", placeholder="ex.: -34.906414/  345430.23S/  34°54'30.23''S", key="Latitud_OP_DMS")
    with col2:
        Latitud_OP_decimal = dms_to_decimal(Latitud_OP_DMS)  # Convertir a decimal
        st.text_input("Latitud en Decimales", value=Latitud_OP_decimal, disabled=True, key="Latitud_OP_dec")

    # Entrada para longitud

    col1, col2 = st.columns(2)
    with col1:
        Longitud_OP_DMS = st.text_input(label="Longitud -[Grados Dec. sin (°) ó  DMS sin (0)]",value="", placeholder="ex.: -57.943292/ 575630.91W/  57°56'30.91''W ", key="Longitud_OP_DMS")
    with col2:
        Longitud_OP_decimal = dms_to_decimal(Longitud_OP_DMS)  # Convertir a decimal
        st.text_input("Longitud en Decimales", value=Longitud_OP_decimal, disabled=True, key="Longitud_OP_dec")

    Elevacion_OP = st.text_input(label="Elevación [m]", value="", key="Elevacion_OP", placeholder="ex.:  15.25 ")
    st.divider()

    st.markdown("Coordenadas del Extremo de Pista")

    # Entrada para latitud del extremo
    col1, col2 = st.columns(2)
    with col1:
        Latitud_EXT_DMS = st.text_input("Latitud - Ext. de Pista [Grados Dec. sin (°) ó  DMS sin (0)]",
                                       value="", placeholder="ex.: -34.906414/ 345430.23S/  34°54'30.23''S", key="Latitud_EXT_DMS")
    with col2:
        Latitud_EXT_decimal = dms_to_decimal(Latitud_EXT_DMS)  # Convertir a decimal
        st.text_input("Latitud en Decimales", value=Latitud_EXT_decimal, disabled=True, key="Latitud_EXT_dec")

    # Entrada para longitud del extremo
    col1, col2 = st.columns(2)
    with col1:
        Longitud_EXT_DMS = st.text_input("Longitud - Ext. de Pista [Grados Dec. sin (°) ó  DMS sin (0)]",
                                        value="", placeholder="ex.: -57.943292/ 575630.91W/  57°56'30.91''W", key="Longitud_EXT_DMS")
    with col2:
        Longitud_EXT_decimal = dms_to_decimal(Longitud_EXT_DMS)  # Convertir a decimal
        st.text_input("Longitud en Decimales", value=Longitud_EXT_decimal, disabled=True, key="Longitud_EXT_dec")

    Elevacion_EXT = st.text_input("Elevación - Extremo de Pista [m]", value="", key="Elevacion_EXT", placeholder="ex.:  15.25 ")

    st.divider()

    st.markdown("__Datos Operativos__")
    t_aproximacion = st.selectbox('Tipo de Aproximación', ['Visual', 'No Precision', 'Precision CAT I', 'Precision CAT II o III'])
    n_clave = st.selectbox('N° de Clave de Referencia de Aeródromo', ['1', '2', '3', '4'])
    ref_SHI = st.selectbox('Elevación de Referencia de la Superficie Horizontal Interna (SHI)', ['RWY - THR', 'Punto Medio', 'RWY - Extremo'])
    st.divider()

    # Botón para generar el archivo
    if st.button("Generar .kml", key="boton_kml"):
        contenido = crear_genslo(nombre_ad, Pista, Longitud_OP_decimal, Latitud_OP_decimal,
                                 Elevacion_OP, Longitud_EXT_decimal, Latitud_EXT_decimal,
                                 Elevacion_EXT, ancho_Pista, t_aproximacion,
                                 n_clave, ref_SHI)

        st.download_button(
            label="Descargar archivo",
            data=documentoFinalKml,
            file_name=f" {nombreFinal}.kml",
            mime="text/plain",
            key="descargar_kml"
        )

    base_informe = '''
    **************************************************************
    *                        INFORME                             *
    **************************************************************
          Tipo de Aproximacion: ''' + t_aproximacion + '''
    *  _______________________________________________________   *
    * |             --> ''' + 'Sentido Operación' + ''' -->>                |  *
      |   Sentido Operación             Sentido Operación     |  
    * |   ==                                               == |  *
    * |   ==     __   ___  ___   ___   ___   ___   __      == |  *
    * |   ==                                               == |  *
    * |_______________________________________________________|  *
    *                                                            *
    *                                                            *
         Aeropuerto: ''' + nombre_ad + '''                       
    *                                                            *
    *    --- Coordenadas de Umbrales (Geográficas Dec.) ---      *
    *    Aproximación                                            *
          Latitud:   ''' + str(Latitud_OP_decimal) + '''°                   
          Longitud:  ''' + str(Longitud_OP_decimal) + '''°                   
          Elevación: ''' + Elevacion_OP + '''m                    
    *                                                            *
    *    Extremo                                                 *
          Latitud:   ''' + str(Latitud_EXT_decimal) + '''°                   
          Longitud:  ''' + str(Longitud_EXT_decimal) + '''°                   
          Elevación: ''' + Elevacion_EXT + '''m                    
    *                                                            *
    *     ------ Referencia Sup. Horizontal Interna ------       *
          Referencia: ''' + ref_SHI + '''                           
    *                                                            *
          Ancho de Pista: ''' + ancho_Pista + '''m
    *                                                            *
    *                                                            *
          N° Clave: ''' + n_clave + '''                       
    *                                                            *
    **************************************************************  '''

    st.download_button(
        label="Descargar Informe",
        data=base_informe,
        file_name=f" {nombre_ad}.txt",
        mime="text/plain",
        key="descargar_informe"
    )
    

if __name__ == '__main__':
    main()



