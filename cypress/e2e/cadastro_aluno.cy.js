describe("Cadastro de Aluno", ()=>{
    it("Deve cadastrar um novo aluno e retornar uma mensagem de sucesso", ()=>{
        cy.visit("http://127.0.0.1:8000/cadastro")
        // npm install --save-dev @types/cypress
        cy.get("input[name='nome']").type("João da Silva")
        cy.get("input[name='matricula']").type("20221IMI001")
        cy.get("input[name='email']").type("joao.silva@example.com")
        cy.get("input[name='senha']").type("senha123")
        cy.get("input[name='conf_senha']").type("senha123")
        cy.get("button[type='submit']").click()
        cy.contains("Sucesso!").should('be.visible')
    })
})

describe("Login de Aluno", ()=>{
    it("Deve realizar o login de um aluno cadastrado", ()=>{
        cy.visit("http://127.0.0.1:8000/login")
        cy.get("input[name='matricula']").type("20221IMI001")
        cy.get("input[name='senha']").type("senha123")
        cy.get("button[type='submit']").click()
        cy.contains("Bem-vindo, João da Silva!").should('be.visible')
    })
})