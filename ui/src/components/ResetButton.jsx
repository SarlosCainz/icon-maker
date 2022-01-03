import {Button} from "react-bulma-components";

function ResetButton({onClick}) {
    return (
        <Button renderAs="a" size="small" color="dark" rounded={true} ml={3} onClick={onClick}>Reset</Button>
    );
}

export default ResetButton;