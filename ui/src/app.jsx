import React, {useState} from 'react'
import "bulma/css/bulma.min.css";
import Header from "./components/Header";
import Body from "./components/Body";
import Footer from "./components/Footer";

export const AppContext = React.createContext();

function App() {
    const [showBurger, setShowBurger] = useState(false);
    const [resetAll, setResetAll] = useState(0);

    const appContext = {
        resetAll: {
            value: resetAll,
            do: () => {
                const now = new Date();
                setResetAll(now.getTime());
                setShowBurger(false);
            }
        },
        burgerMenu: {
            value: showBurger,
            set: setShowBurger,
            toggle: () => {setShowBurger(!showBurger)}
        }
    }

    return (
        <>
            <AppContext.Provider value={appContext}>
                <Header />
                <Body />
                <Footer />
            </AppContext.Provider>
        </>
    );
}

export default App;
