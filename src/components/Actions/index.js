import React from "react";
import {View,Text, StyleSheet, TouchableOpacity, ScrollView, Image} from "react-native";

import {AntDesign} from '@expo/vector-icons'

//Criando os botões de ação da tela inicial (pix, qr code, cartão virtual e empréstimo)
export default function Actions () {
    return (
        <ScrollView style={styles.container} horizontal={true} showsHorizontalScrollIndicator={false}>
            <TouchableOpacity activeOpacity={0.6} style={styles.actionButton}>
                <View style={styles.areaButton}>
                    <Image source={require('../../../assets/image-pix.png')}
                    style={styles.imageButton}/>
                </View>
                <Text style={styles.labelButton}>Pix</Text>
            </TouchableOpacity>


            <TouchableOpacity activeOpacity={0.6} style={styles.actionButton}>
                <View style={styles.areaButton}>
                    <Image source={require('../../../assets/image-qrCode.png')}
                    style={styles.imageButton}/>
                </View>
                <Text style={styles.labelButton}>QR Code</Text>
            </TouchableOpacity>

            
            <TouchableOpacity activeOpacity={0.6} style={styles.actionButton}>
                <View style={styles.areaButton}>
                    <Image source={require('../../../assets/image-virtualCard.png')}
                    style={styles.imageButton}/>
                </View>
                <Text style={styles.labelButton}>Card</Text>
            </TouchableOpacity>


            <TouchableOpacity activeOpacity={0.6} style={styles.actionButton}>
                <View style={styles.areaButton}>
                    <Image source={require('../../../assets/image-loan.png')}
                    style={styles.imageButton}/>
                </View>
                <Text style={styles.labelButton}>Loan</Text>
            </TouchableOpacity>
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container:{
        color: '#232323',
        maxHeight: 95,
        marginBottom: 14,
        marginTop: 18,
        paddingEnd: 14,
        paddingStart: 14,
    },
    actionButton:{
        backgroundColor: '#1E1E1E',
        alignItems: 'center',
        marginRight: 30,
        borderRadius: 50,
        height: 70,
        width: 70,
        justifyContent: 'center'
    },
    // AreaButton:{
    //     backgroundColor: '#ecf0f1',
    //     height: 60,
    //     width: 60,
    //     borderRadius: 30,
    //     justifyContent: 'center',
    //     alignItems: 'center'
    // },
    labelButton:{
        color: '#FFF',
    },
    imageButton:{
        marginTop: 40,
        marginBottom: 20
    }
})
