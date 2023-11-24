import { StyleSheet, Text, View } from 'react-native';
import Header from '../../components/Header';
import Balance from '../../components/Balance';
import Actions from '../../components/Actions';
import GiftCards from '../../components/giftCards';
import Invoice from '../../components/Invoice';
import Inicial from '../../components/Inicial';


export default function App() {
  return (
    <View style={styles.container}>
        <Header name="Giovanna Vieira"/>
      <Balance saldo="10.000,00"/>
      <Actions/>
      <GiftCards/>
      <Invoice fatura="1.250,00"/>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#171717',
  },
});
