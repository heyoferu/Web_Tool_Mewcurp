// Cargar la memoria desde localStorage al inicio
let mem = JSON.parse(localStorage.getItem('mem')) || [];

function MS() { 
    let value = document.getElementById('result_display').value;
    if (value) {
        mem.push(value);
        localStorage.setItem('mem', JSON.stringify(mem));
    } else {
        alert("Por favor ingrese un valor a guardar.");
    }
}

function MR() {
    if (mem.length > 0) {
        let valorRecuperado = mem.pop();
        document.getElementById('cal_display').value += valorRecuperado;
        localStorage.setItem('mem', JSON.stringify(mem)); 
    } else {
        alert("No existen valores guardados en memoria!");
    }
}

function MC() {
    mem = [];
    localStorage.removeItem('mem');
    console.log("Memoria borrada"); 
}


// Función para insertar números y operadores en el textarea
function insert(val) {
    var display = document.getElementById('cal_display');

    if (display.value === "0") {
        display.value = val; // Reemplaza "0" por el nuevo valor
    } else {
        display.value += val; // Añade el valor actual
    }
}

// Función para limpiar el textarea
function clear_screen() {
    document.getElementById('cal_display').value = '0';
}

function r() {
    let display = document.getElementById('cal_display');
    let display_splited = display.value.split('');
    display_splited.pop();
    display.value = display_splited.join('');
    if (display.value === '') {
        display.value = '0';
    }
}


class Node {
    constructor(value) {
        this.value = value;
        this.left = null;
        this.right = null;
    }
}

function buildTree(expression) {
    let stack = [];
    let operators = [];
    let precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '%': 2,
        '(': 0  // Menor precedencia para asegurar que se procese al final
    };

    function createNode(operator) {
        let node = new Node(operator);
        node.right = stack.pop();
        node.left = stack.pop();
        stack.push(node);
    }

    for (let i = 0; i < expression.length; i++) {
        let char = expression[i];

        if (char === ' ') continue; // Ignorar espacios

        if (!isNaN(char) || char === '.') {
            let num = "";
            while (i < expression.length && (!isNaN(expression[i]) || expression[i] === '.')) {
                num += expression[i];
                i++;
            }
            i--; // Retrocede uno porque incrementa de más
            stack.push(new Node(num));
        } else if (char === '(') {
            operators.push(char);
        } else if (char === ')') {
            while (operators.length && operators[operators.length - 1] !== '(') {
                createNode(operators.pop());
            }
            if (operators.length && operators[operators.length - 1] === '(') {
                operators.pop(); // Elimina el '('
                // Crear un nodo especial para los paréntesis
                let parenNode = new Node('( )');
                parenNode.left = stack.pop();
                stack.push(parenNode);
            }
        } else if (char in precedence) {
            while (operators.length && operators[operators.length - 1] !== '(' &&
                   precedence[char] <= precedence[operators[operators.length - 1]]) {
                createNode(operators.pop());
            }
            operators.push(char);
        }
    }

    while (operators.length) {
        createNode(operators.pop());
    }

    return stack.pop();
}

function generateTree() {
    const expression = document.getElementById("cal_display").value;
    const tree = buildTree(expression);
    drawTree(tree);
}

function drawTree(root) {
    const svg = d3.select("svg");
    svg.selectAll("*").remove();

    // Definir un grupo (g) para aplicar el zoom y pan
    const g = svg.append("g");

    let data = convertTreeToD3Format(root);
    let rootD3 = d3.hierarchy(data);

    let treeLayout = d3.tree().size([400, 400]);
    treeLayout(rootD3);

    // Animación de las líneas (aristas)
    const lines = g.selectAll('line')
        .data(rootD3.links())
        .enter()
        .append('line')
        .attr('x1', d => d.source.x + 50)
        .attr('y1', d => d.source.y + 50)
        .attr('x2', d => d.source.x + 50)  // Comienzan desde el mismo punto para efecto de animación
        .attr('y2', d => d.source.y + 50)
        .style('stroke', 'green')
        .transition()
        .duration(1000)
        .attr('x2', d => d.target.x + 50)
        .attr('y2', d => d.target.y + 50);

    // Animación de los nodos (círculos)
    const circles = g.selectAll('circle')
        .data(rootD3.descendants())
        .enter()
        .append('circle')
        .attr('cx', d => d.x + 50)
        .attr('cy', d => d.y + 50)
        .attr('r', 0)  // Comienzan con radio 0
        .style('fill', 'white')
        .style('stroke', 'green')
        .transition()
        .duration(1000)
        .attr('r', 20);  // Expanden al radio original

    // Texto dentro de los nodos
    const texts = g.selectAll('text')
        .data(rootD3.descendants())
        .enter()
        .append('text')
        .attr('x', d => d.x + 50)
        .attr('y', d => d.y + 50)
        .attr('dy', '.35em')
        .attr('text-anchor', 'middle')
        .text(d => d.data.value)
        .style('opacity', 0)  // Empieza invisible
        .transition()
        .delay(1000)  // Aparece después de que se muestran los círculos
        .style('opacity', 1);

    // Agregar funcionalidad de zoom
    const zoom = d3.zoom()
        .scaleExtent([0.5, 5])  // Limitar el zoom entre 0.5x y 5x
        .on('zoom', (event) => {
            g.attr('transform', event.transform);  // Aplicar transformación (escalar/desplazar)
        });

    // Aplicar zoom al svg
    svg.call(zoom);
}


function convertTreeToD3Format(node) {
    if (!node) return null;
    return {
        value: node.value,
        children: [
            convertTreeToD3Format(node.left),
            convertTreeToD3Format(node.right)
        ].filter(n => n !== null)
    };
}