import React from 'react'
import axios from 'axios'
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react"
import { Col, Container, Row, Button, Form } from 'react-bootstrap';
import { useNavigate } from "react-router-dom";

import '../App.css'


export default function Customer() {

  let params = useParams();
  const url = "http://127.0.0.1:5000/customer/" + params.customerId
  const [incidents, setIncidents] = useState(null)
  let navigate = useNavigate()


  useEffect(() => {
    axios.get(url).then(response => {
      setIncidents(response.data)
      console.log(response.data)
    })
  }, [url])



  if (incidents) {
    return (
      <Container fluid>
        <Row className='m-3'>
            <Col className='d-flex justify-content-end'>
                <Button variant="success" onClick={() => navigate('/customer/' + params.customerId + '/createincident')}>New Incident</Button>
            </Col>
        </Row>
        {incidents.map((incident) =>
          <Row className='text-center m-3' onClick={() => navigate('/incident/' + incident.id)}>
            <Col className='incident' xs={{offset: 1, span: 10}} md={{offset: 2, span: 8}} lg={{offset: 3, span: 6}}>{incident.date + " - " + incident.type}</Col>
          </Row>
        )}
      </Container>
    )
  }
  else
    return (
      <div>Loading ...</div>
    )
}
