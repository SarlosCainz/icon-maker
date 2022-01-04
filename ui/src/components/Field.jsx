import {useCallback} from "react";
import {Element, Form} from "react-bulma-components";

function Field({label, children, className, note}) {
    const Note = useCallback( (note) => {
        if (note !== void 0) {
            return <Form.Label textSize={7} ml={2}>{note}</Form.Label>
        }
    }, [note]);


    return (
        <Form.Field className={className}>
            <Form.Label>{label}</Form.Label>
            {Note(note)}
            <Form.Field.Body ml={2} alignItems="center">{children}</Form.Field.Body>
        </Form.Field>
    );
}

export default Field;
