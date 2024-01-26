use std::fs::File;
use std::io::{BufRead, BufReader};

#[derive(Debug)]
#[allow(dead_code)]
struct Record {
    conditions: String,
    rules: Vec<usize>,
    cache: Vec<i64>,
}

impl Record {
    fn new(conditions: String, rules: Vec<usize>) -> Record {
        let cache_size = conditions.len() * rules.len();
        Record {
            conditions,
            rules,
            cache: vec![-1; cache_size],
        }
    }

    fn count_from(&mut self, cond_index: usize, rule_index: usize) -> i64 {
        // Calculate the result
        if rule_index == self.rules.len() {
            if cond_index < self.conditions.len() && self.conditions[cond_index..].contains('#') {
                return 0;
            }
            return 1;
        }
        if cond_index >= self.conditions.len() {
            if rule_index == self.rules.len() {
                return 1;
            }
            return 0;
        }

        // Check if the result is already cached
        let result = self.cache[self.conditions.len() * rule_index + cond_index];
        if result != -1 {
            return result;
        }

        let mut counter = 0;
        let condition = self.conditions.as_bytes()[cond_index] as char;
        let rule = self.rules[rule_index];

        // Assume '?' is a '.'
        if condition == '.' || condition == '?' {
            counter += self.count_from(cond_index + 1, rule_index);
        }
        // Assume '?' is a '#'
        if condition == '#' || condition == '?' {
            if cond_index + rule <= self.conditions.len() // Enough chars available
                && !self.conditions[cond_index..cond_index + rule].contains('.')
            // No dot in range
            {
                let would_consume_all = cond_index + rule == self.conditions.len();
                if would_consume_all || self.conditions.as_bytes()[cond_index + rule] as char != '#'
                {
                    counter += self.count_from(cond_index + rule + 1, rule_index + 1)
                }
            }
        }
        self.cache[self.conditions.len() * rule_index + cond_index] = counter;
        counter
    }
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
        records.push(Record::new(conditions.to_string(), rules));
    }

    let part1: i64 = records
        .iter_mut()
        .map(|record| record.count_from(0, 0))
        .sum();

    let mut part2: i64 = 0;
    for record in records.iter() {
        let condition = std::iter::repeat(record.conditions.clone())
            .take(5)
            .collect::<Vec<String>>()
            .join("?");
        part2 += Record::new(condition, record.rules.repeat(5)).count_from(0, 0);
    }
    println!("Part 1 {:?}", part1);
    println!("Part 2 {:?}", part2);
}
