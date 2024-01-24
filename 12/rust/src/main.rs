use hashbrown::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

#[derive(Debug)]
#[allow(dead_code)]
struct Record {
    conditions: String,
    rules: Vec<usize>,
}

fn simple_count(conditions: &str, rules: &[usize]) -> i64 {
    if rules.len() == 0 {
        if conditions.contains('#') {
            return 0;
        }
        return 1;
    }
    if conditions.len() == 0 {
        if rules.len() == 0 {
            return 1;
        }
        return 0;
    }
    let mut counter = 0;
    let condition = conditions.chars().next().unwrap();
    let rule = rules[0];

    // Assume '?' is a '.'
    if condition == '.' || condition == '?' {
        counter += simple_count(&conditions[1..], rules);
    }
    // Assume '?' is a '#'
    if condition == '#' || condition == '?' {
        let enough_chars = rule <= conditions.len();
        let no_dot_in_range = conditions.chars().take(rule).all(|c| c != '.');
        let would_consume_all = rule == conditions.len();
        let no_spring_after_range = conditions.chars().nth(rule).unwrap_or('#') != '#';
        if enough_chars && no_dot_in_range && (would_consume_all || no_spring_after_range) {
            counter += simple_count(conditions.get(rule + 1..).unwrap_or(""), &rules[1..]);
        }
    }
    counter
}

fn memoized_count(
    conditions: &str,
    rules: &[usize],
    cache: &mut HashMap<(String, Vec<usize>), i64>,
) -> i64 {
    // Check if the result is already cached
    if let Some(&result) = cache.get(&(conditions.to_string(), rules.to_vec())) {
        return result;
    }

    // Calculate the result
    if rules.len() == 0 {
        if conditions.contains('#') {
            return 0;
        }
        return 1;
    }
    if conditions.len() == 0 {
        if rules.len() == 0 {
            return 1;
        }
        return 0;
    }
    let mut counter = 0;
    let condition = conditions.chars().next().unwrap();
    let rule = rules[0];

    // Assume '?' is a '.'
    if condition == '.' || condition == '?' {
        counter += memoized_count(&conditions[1..], rules, cache);
    }
    // Assume '?' is a '#'
    if condition == '#' || condition == '?' {
        let enough_chars = rule <= conditions.len();
        let no_dot_in_range = conditions.chars().take(rule).all(|c| c != '.');
        let would_consume_all = rule == conditions.len();
        let no_spring_after_range = conditions.chars().nth(rule).unwrap_or('#') != '#';
        if enough_chars && no_dot_in_range && (would_consume_all || no_spring_after_range) {
            counter += memoized_count(conditions.get(rule + 1..).unwrap_or(""), &rules[1..], cache)
        }
    }
    cache.insert((conditions.to_string(), rules.to_vec()), counter);
    counter
}

fn main() {
    let file = File::open("../input").expect("Failed to open file");
    let reader = BufReader::new(file);
    let mut records = Vec::new();
    for line in reader.lines() {
        let line = line.unwrap();
        let mut parts = line.split(" ");
        let conditions = parts.next().unwrap();
        let rules: Vec<usize> = parts
            .next()
            .unwrap()
            .split(",")
            .map(|s| s.parse::<usize>().unwrap())
            .collect();
        records.push(Record {
            conditions: conditions.to_string(),
            rules: rules,
        });
    }

    let part1: i64 = records
        .iter()
        .map(|record| simple_count(&record.conditions, &record.rules))
        .sum();

    let mut cache: HashMap<(String, Vec<usize>), i64> = HashMap::new();
    let mut part2: i64 = 0;
    for record in records.iter() {
        let condition = std::iter::repeat(record.conditions.clone())
            .take(5)
            .collect::<Vec<String>>()
            .join("?");
        part2 += memoized_count(&condition, &record.rules.repeat(5), &mut cache);
    }
    println!("Part 1 {:?}", part1);
    println!("Part 2 {:?}", part2);
}
