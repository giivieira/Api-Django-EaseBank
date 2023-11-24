import React, { startTransition } from "react";
import { View, Text, StyleSheet, ImageBackground } from 'react-native';

// Criando componente que mostra o saldo do usuário
export default function Balance({ saldo }) {
    return (

        <ImageBackground style={styles.container} source={require('../../../assets/quadriculado-fundoCinza.png')}>
        <View >
                <View style={styles.item}>

                    <Text style={styles.itemTitle}>Saldo</Text>
                    <View style={styles.content}>
                        <Text style={styles.currencySymbol}>R$</Text>
                        <Text style={styles.balance}>{saldo}</Text>
                    </View>
                </View>
            
        </View>
        </ImageBackground>
    );
}

//Estilizando o container que guarda as informações
const styles = StyleSheet.create({
    container: {
        // backgroundColor: '#2E2E2E',
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingStart: 18,
        paddingEnd: 18,
        marginTop: -24,
        marginStart: 14,
        marginEnd: 14,
        paddingTop: 22,
        paddingBottom: 22,
        
    },

    //Estilizando as informações contidas no container
    itemTitle: {
        fontSize: 20,
        color: '#FFF'
    },
    content: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    currencySymbol: {
        fontSize: 22,
        color: '#FFF',
        marginRight: 6,
    },
    balance: {
        fontSize: 22,
        color: '#FFF',
    }
})
