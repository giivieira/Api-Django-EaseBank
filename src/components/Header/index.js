import React from "react";
import {View, StyleSheet, Text, StatusBar, TouchableOpacity, Image} from "react-native";
import {Feather} from '@expo/vector-icons'
const statusBarHeight = StatusBar.currentHeight ? StatusBar.currentHeight + 22 : 64;


//Cabeçalho da página inicial (nome do usuátio, ícone...)
export default function Header({ name }) {
    return (
      <View style={styles.container}>
        <View style={styles.content}>
          <View style={styles.containerIcon}>
            <Image source={require('../../../assets/iconBank.png')} />
          </View>
          <Text style={styles.username}>{name}</Text>
          <TouchableOpacity activeOpacity={0.9} style={styles.buttonUser}>
            <Feather name="user" size={27} color="#FFF" />
          </TouchableOpacity>
        </View>
      </View>
    );
  }

//Estilizando o cabeçalho da página inicial
const styles = StyleSheet.create({
    container:{
        backgroundColor: '#171717',
        paddingTop: statusBarHeight,
        flexDirection: 'row',
        paddingStart: 16,
        paddingEnd: 16,
        paddingBottom: 44,
    },
    content:{
        flex: 1,
        alignItems: 'center',
        flexDirection: 'row',
        justifyContent: 'space-between'
    },
    username:{
        fontSize: 18,
        color: '#FFF',
        fontWeight: 'bold',
        
    },
    buttonUser:{
        width: 44,
        height: 44,
        backgroundColor: 'rgba(255, 255, 255, 0.5)',
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 44 / 2,
    }
})
