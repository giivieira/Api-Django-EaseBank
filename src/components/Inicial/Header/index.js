import React, { startTransition } from "react";
import { View, Text, StyleSheet, ImageBackground, StatusBar } from 'react-native';
const statusBarHeight = StatusBar.currentHeight ? StatusBar.currentHeight + 22 : 64;


// Criando componente que mostra o saldo do usuário
export default function Inicial({ }) {
    return (

        <ImageBackground style={styles.container} source={require('../../../assets/quadriculado-fundoCinza.png')}>
        <View >
                <View style={styles.item}>
                    </View>
                </View>
        </ImageBackground>
    );
}

//Estilizando o container que guarda as informações
const styles = StyleSheet.create({
    container: {
        width: 100,
        height: 300
    },

})
