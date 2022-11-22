package main

import (
	"fmt"
	"sync"
)

// Additional parameter 1: wg *sync.WaitGroup to help sync end of all worker routines.
func worker(wg *sync.WaitGroup, id int, jobs <-chan int, results chan<- int) {
	// Addition of wating group to sync all the worker go routines
	defer wg.Done()
	for j := range jobs {
		// Internal GO routine is not needed
		switch j % 3 {
		case 0:
			// Case 0 seemed redundant maybe user wanted to send multiples as per condition.
			// So send j to the results channel.
			results <- j
		// Removal of assignment condition as now we are using local variables.
		// Earlier this case observed 4 times j value being sent, corrected to 2 times.
		case 1:
			results <- j * 2
		case 2:
			results <- j * 3
		}
	}
}

// Converted summing code into another function to make it run as a go routine.
func summer(results <-chan int, sumPointer *int64) {
	for r := range results {
		*sumPointer += int64(r)
	}
}

func main() {
	// Added waiting group to sync all worker node calls.
	wg := &sync.WaitGroup{}
	// Added waiting group to sync all worker node calls.
	jobs := make(chan int)
	results := make(chan int)

	// Instead of sending jobs to multiple go subroutines now using one go subroutine
	// to generate jobs.
	go func() {
		for i := 1; i <= 1000000000; i++ {
			if i%2 == 0 {
				i += 99
			}
			// fmt.Printf("%d Job received %d\n", jobsSent, i)
			jobs <- i
		}
		// We close the jobs in the go subroutine which sends the jobs, rather than closing
		// in the main function.
		close(jobs)
	}()

	for w := 1; w < 1000; w++ {
		// Adding worker to the wait group.
		wg.Add(1)
		go worker(wg, w, jobs, results)
	}

	// sum variable has been converted to int64 as it started to overflow.
	var sum int64 = 0
	go summer(results, &sum)
	// Waiting for all workers to finish.
	wg.Wait()
	// Close the results channel.
	close(results)
	fmt.Println(sum)
}
