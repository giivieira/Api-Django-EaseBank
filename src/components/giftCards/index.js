import React, { startTransition } from "react";
import { View, Text, StyleSheet, ImageBackground, TouchableOpacity, Image } from 'react-native';

export default function GiftCards({ }) {
    return (
        <View style={styles.container}>
            <Text style={styles.itemTitle}>Compre gift cards</Text>
            <View style={styles.AreaGiftButton}>
                <TouchableOpacity activeOpacity={0.6} style={styles.giftButton}>
                    <Image source={require('../../../assets/ifood.png')} />
                </TouchableOpacity>

                <TouchableOpacity activeOpacity={0.6} style={styles.giftButton}>
                    <Image source={require('../../../assets/freeFire.png')} />
                </TouchableOpacity>
                <TouchableOpacity activeOpacity={0.6} style={styles.giftButton}>
                    <Image source={require('../../../assets/amazon.png')} />
                </TouchableOpacity>
            </View>
        </View>

    );
}

const styles = StyleSheet.create({
    container: {
        backgroundColor: '#1E1E1E',
        height: 150,
        width: 365,
        marginStart: 14,
        marginEnd: 14,
        padding: 10,
        display: 'flex',
        justifyContent: "center",
        marginTop: 20
    },
    itemTitle: {
        color: '#FFF',
        fontSize: 18,
        marginTop: 10
    },
    giftButton: {
        backgroundColor: '#232323',
        // marginRight: 30,
        margin: 20,
        borderRadius: 50,
        height: 60,
        width: 60,
        justifyContent: 'center',
        alignItems: 'center',
    },
    AreaGiftButton: {
        flexDirection: "row",
        justifyContent: "center",
        alignItems: "center"
    }
})

