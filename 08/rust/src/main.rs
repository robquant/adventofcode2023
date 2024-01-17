use num::integer::lcm;
use regex::Regex;
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

enum Direction {
    Left,
    Right,
}

#[derive(Debug)]
struct Node {
    left: String,
    right: String,
}

// fn count_steps(
//     nodes: &HashMap<String, Node>,
//     start_node: &String,
//     steps: &Vec<Direction>,
//     stop_condition: impl Fn(&String) -> bool,
// ) -> i64 {
//     let mut current_node = start_node.clone();
//     let mut counter = 0;
//     for step in steps.iter().cycle() {
//         let node = nodes.get(&current_node).unwrap();
//         match step {
//             Direction::Left => current_node = node.left.clone(),
//             Direction::Right => current_node = node.right.clone(),
//         }
//         counter += 1;
//         if stop_condition(&current_node) {
//             break;
//         }
//     }
//     counter
// }

// Optimized with less cloning
fn count_steps(
    nodes: &HashMap<String, Node>,
    start_node: &String,
    steps: &Vec<Direction>,
    stop_condition: impl Fn(&String) -> bool,
) -> i64 {
    let mut current_node = start_node;
    let mut counter = 0;
    for step in steps.iter().cycle() {
        let node = &nodes[current_node];
        match step {
            Direction::Left => current_node = &node.left,
            Direction::Right => current_node = &node.right,
        }
        counter += 1;
        if stop_condition(&current_node) {
            break;
        }
    }
    counter
}

fn parse() -> (Vec<Direction>, HashMap<String, Node>) {
    let file = File::open("../input").expect("Failed to open file");
    let reader = BufReader::new(file);
    let mut lines = reader.lines();

    let steps_string = lines.next().unwrap().unwrap();
    let steps: Vec<Direction> = steps_string
        .chars()
        .map(|step| match step {
            'L' => Direction::Left,
            'R' => Direction::Right,
            _ => panic!("Invalid direction"),
        })
        .collect();

    // Skip the second line
    lines.next();

    let mut nodes: HashMap<String, Node> = HashMap::new();
    // Each line looks like this:  LST = (PVJ, DPR)
    let re = Regex::new(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)").unwrap();
    // Iterate over the remaining lines
    for line in lines {
        if let Ok(line) = line {
            if let Some(captures) = re.captures(&line) {
                let start = captures.get(1).unwrap().as_str().to_string();
                let left = captures.get(2).unwrap().as_str().to_string();
                let right = captures.get(3).unwrap().as_str().to_string();
                nodes.insert(start, Node { left, right });
            }
        }
    }
    return (steps, nodes);
}

fn main() {
    let (steps, nodes) = parse();
    // Part 1
    let stop_at_zzz = |node: &String| node == "ZZZ";
    let part1 = count_steps(&nodes, &"AAA".to_string(), &steps, stop_at_zzz);
    println!("Part 1: {}", part1);

    // Part 2
    let start_nodes = nodes.keys().filter(|key| key.ends_with('A'));
    let stop_when_it_ends_with_z = |node: &String| node.ends_with('Z');
    let step_counts =
        start_nodes.map(|node| count_steps(&nodes, node, &steps, stop_when_it_ends_with_z));

    let total_steps = step_counts.fold(1, |acc, x| lcm(acc, x));
    println!("Part 2: {}", total_steps);
}
