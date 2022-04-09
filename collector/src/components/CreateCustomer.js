import axios from 'axios';
import React, { useState } from 'react'
import { Container, Form, Row, Col, Button } from 'react-bootstrap';


export default function CreateCustomer() {


    const [base64, setBase64] = useState(null)
    const [formValue, setFormValue] = useState({
        name: "",
        date: "",
    });

    const imageChange = (event) => {
        let image = event.target.files[0]
        let reader = new FileReader()
        reader.readAsDataURL(image)
        reader.onload = function () {
            setBase64(reader.result)
        }

    }

    const handleChange = (event) => {
        setFormValue({
          ...formValue,
          [event.target.name]: event.target.value
        });
      }

    const handleSubmit = (event) => {

        const data = {
            name: formValue.name,
            data: formValue.date,
            logo: base64
        }
        
        axios.post('http://127.0.0.1:5000/customer/create', data)
            .then(response => console.log(response.status));
        event.preventDefault()
    }

    return (
        <Container>
            <Form onSubmit={handleSubmit}>
                <Row className='mt-5'>
                    <h1>Create new Customer</h1>
                    <Col className='mt-5' xs="12" lg="6">
                        <Form.Group className="mb-3">
                            <Form.Label>Name</Form.Label>
                            <Form.Control name='name' placeholder="" onChange={handleChange}/>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Logo</Form.Label>
                            <Form.Control type="file" size='md' onChange={imageChange}></Form.Control>
                        </Form.Group>
                    </Col>
                    <Row className='mt-5'>
                        <Col className="d-grid d-md-none">
                            <Button variant="primary" type="submit" size="lg">Submit</Button>
                        </Col>
                        <Col className="d-none d-md-flex">
                            <Button variant="primary" type="submit">Submit</Button>
                        </Col>
                    </Row>
                </Row>
            </Form>
        </Container>
    )
}
