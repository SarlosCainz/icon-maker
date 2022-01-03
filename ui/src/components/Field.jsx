import {Form} from "react-bulma-components";

function Field({label, children, className}) {
    return (
        <Form.Field className={className}>
            <Form.Label>{label}</Form.Label>
            <Form.Field.Body ml={2} alignItems="center">{children}</Form.Field.Body>
        </Form.Field>
    );
}

export default Field;
